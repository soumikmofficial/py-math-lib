pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: '', description: 'Branch to build (leave empty for auto-detection)')
        choice(name: 'RELEASE_MODE', choices: ['auto', 'manual', 'skip'], description: 'Release mode')
        choice(name: 'VERSION_TYPE', choices: ['patch', 'minor', 'major'], description: 'Version bump type (for manual release)')
        booleanParam(name: 'DRY_RUN', defaultValue: false, description: 'Perform a dry run without publishing')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip running tests')
    }

    
    
    environment {
        // Python environment
        PYTHON_VERSION = '3'
        VIRTUAL_ENV = "${WORKSPACE}/venv"
        PATH = "${VIRTUAL_ENV}/bin:${PATH}"
        
        // Package registry configuration
        PYPI_REGISTRY = 'https://pypi.org/'
        TEST_PYPI_REGISTRY = 'https://test.pypi.org/'
        
        // Git configuration
        GIT_AUTHOR_NAME = 'Jenkins CI'
        GIT_AUTHOR_EMAIL = 'jenkins@example.com'
        GIT_COMMITTER_NAME = 'Jenkins CI'
        GIT_COMMITTER_EMAIL = 'jenkins@example.com'
        
        // Credentials
        GITHUB_TOKEN = credentials('github-token')
        PYPI_TOKEN = credentials('pypi-token')
        
        // Build information
        BUILD_TIMESTAMP = sh(script: "date '+%Y%m%d-%H%M%S'", returnStdout: true).trim()
    }
    
    stages {
        stage('Initialize') {
            steps {
                script {
                    // Determine branch name
                    if (params.BRANCH_NAME) {
                        env.TARGET_BRANCH = params.BRANCH_NAME
                    } else {
                        env.TARGET_BRANCH = env.GIT_BRANCH ?: sh(
                            script: 'git rev-parse --abbrev-ref HEAD',
                            returnStdout: true
                        ).trim()
                    }
                    
                    // Clean branch name (remove origin/ prefix if present)
                    env.TARGET_BRANCH = env.TARGET_BRANCH.replaceAll('origin/', '')
                    
                    // Get commit hash
                    env.COMMIT_HASH = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    
                    // Get current version from git tags
                    def currentVersion = sh(
                        script: "git describe --tags --abbrev=0 2>/dev/null || echo 'v0.0.0'",
                        returnStdout: true
                    ).trim().replaceAll('v', '')
                    env.CURRENT_VERSION = currentVersion
                    
                    // Determine release channel
                    if (env.TARGET_BRANCH ==~ /(main|master)/) {
                        env.RELEASE_CHANNEL = 'latest'
                    } else if (env.TARGET_BRANCH ==~ /(develop|staging)/) {
                        env.RELEASE_CHANNEL = 'beta'
                    } else {
                        env.RELEASE_CHANNEL = 'none'
                    }
                    
                    // Display build information
                    echo """
                    ===== Build Information =====
                    Branch: ${env.TARGET_BRANCH}
                    Commit: ${env.COMMIT_HASH}
                    Current Version: ${env.CURRENT_VERSION}
                    Release Mode: ${params.RELEASE_MODE}
                    Release Channel: ${env.RELEASE_CHANNEL}
                    Dry Run: ${params.DRY_RUN}
                    Build Timestamp: ${env.BUILD_TIMESTAMP}
                    =============================
                    """
                }
                
                // Checkout the target branch
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: env.TARGET_BRANCH]],
                    extensions: [
                        [$class: 'CleanBeforeCheckout'],
                        [$class: 'CloneOption', depth: 0, noTags: false, shallow: false]
                    ],
                    userRemoteConfigs: [[
                        url: env.GIT_URL ?: 'https://github.com/yourusername/py-math-lib.git',
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "Setting up Python ${PYTHON_VERSION} virtual environment..."
                    python${PYTHON_VERSION} -m venv ${VIRTUAL_ENV}
                    . ${VIRTUAL_ENV}/bin/activate
                    
                    echo "Upgrading pip and setuptools..."
                    pip install --upgrade pip setuptools wheel
                    
                    echo "Installing package in editable mode with dev dependencies..."
                    pip install -e ".[dev]"
                    
                    echo "Python environment info:"
                    python --version
                    pip --version
                    pip list
                '''
            }
        }
        
        stage('Quality Checks') {
            parallel {
                stage('Lint') {
                    steps {
                        sh '''
                            echo "Running flake8 linter..."
                            . ${VIRTUAL_ENV}/bin/activate
                            flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
                        '''
                    }
                }
                
                stage('Type Check') {
                    steps {
                        sh '''
                            echo "Running mypy type checker..."
                            . ${VIRTUAL_ENV}/bin/activate
                            mypy src/py_math_lib
                        '''
                    }
                }
                
                stage('Format Check') {
                    steps {
                        sh '''
                            echo "Checking code formatting with black..."
                            . ${VIRTUAL_ENV}/bin/activate
                            black --check src/ tests/
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            when {
                expression { !params.SKIP_TESTS }
            }
            steps {
                sh '''
                    echo "Running pytest with coverage..."
                    . ${VIRTUAL_ENV}/bin/activate
                    pytest
                '''
            }
            post {
                always {
                    // Archive test results
                    junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
                    
                    // Publish coverage reports
                    publishHTML target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ]
                }
            }
        }
        
        stage('Build') {
            steps {
                sh '''
                    echo "Building distribution packages..."
                    . ${VIRTUAL_ENV}/bin/activate
                    
                    # Clean previous builds
                    rm -rf dist/ build/ *.egg-info
                    
                    # Build source distribution and wheel
                    python -m build
                    
                    # List built packages
                    echo "Built packages:"
                    ls -la dist/
                '''
            }
        }
        
        stage('Release Decision') {
            when {
                expression { 
                    params.RELEASE_MODE != 'skip' && 
                    env.RELEASE_CHANNEL != 'none' &&
                    !params.DRY_RUN
                }
            }
            steps {
                script {
                    // Check if there are changes since last tag
                    def hasChanges = sh(
                        script: '''git diff --quiet HEAD $(git describe --tags --abbrev=0 2>/dev/null || echo 'HEAD~1') || echo 'true' ''',
                        returnStdout: true
                    ).trim() == 'true'

                    
                    if (!hasChanges) {
                        echo "No changes detected since last release. Skipping release."
                        env.SHOULD_RELEASE = 'false'
                    } else {
                        env.SHOULD_RELEASE = 'true'
                        
                        if (params.RELEASE_MODE == 'manual') {
                            // Manual release - ask for confirmation
                            def nextVersion = calculateNextVersion(
                                env.CURRENT_VERSION, 
                                params.VERSION_TYPE
                            )
                            
                            input message: """
                                Confirm manual release:
                                Current version: ${env.CURRENT_VERSION}
                                Next version: ${nextVersion}
                                Version type: ${params.VERSION_TYPE}
                                Release channel: ${env.RELEASE_CHANNEL}
                                
                                Proceed with release?
                            """, ok: 'Release'
                            
                            env.NEXT_VERSION = nextVersion
                        }
                    }
                }
            }
        }
        
        stage('Release') {
            when {
                expression { 
                    env.SHOULD_RELEASE == 'true' &&
                    !params.DRY_RUN
                }
            }
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'github-token', variable: 'GH_TOKEN'),
                        string(credentialsId: 'pypi-token', variable: 'TWINE_PASSWORD')
                    ]) {
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            
                            # Configure git
                            git config user.name "${GIT_AUTHOR_NAME}"
                            git config user.email "${GIT_AUTHOR_EMAIL}"
                            
                            # Set up PyPI credentials
                            export TWINE_USERNAME="__token__"
                        '''
                        
                        if (params.RELEASE_MODE == 'auto') {
                            // Automatic release using python-semantic-release
                            sh '''
                                . ${VIRTUAL_ENV}/bin/activate
                                
                                echo "Running semantic-release..."
                                export GH_TOKEN="${GH_TOKEN}"
                                
                                # Run semantic-release
                                semantic-release publish \
                                    --hvcs=github \
                                    --hvcs-token="${GH_TOKEN}"
                            '''
                        } else if (params.RELEASE_MODE == 'manual') {
                            // Manual release
                            sh """
                                . ${VIRTUAL_ENV}/bin/activate
                                
                                echo "Performing manual release to version ${env.NEXT_VERSION}..."
                                
                                # Update version in pyproject.toml
                                sed -i 's/version = .*/version = "${env.NEXT_VERSION}"/' pyproject.toml
                                
                                # Commit version change
                                git add pyproject.toml
                                git commit -m "chore(release): ${env.NEXT_VERSION} [skip ci]"
                                
                                # Create and push tag
                                git tag -a "v${env.NEXT_VERSION}" -m "Release v${env.NEXT_VERSION}"
                                git push origin ${env.TARGET_BRANCH}
                                git push origin "v${env.NEXT_VERSION}"
                                
                                # Upload to PyPI
                                if [ "${env.RELEASE_CHANNEL}" = "beta" ]; then
                                    echo "Uploading to Test PyPI..."
                                    twine upload --repository testpypi dist/*
                                else
                                    echo "Uploading to PyPI..."
                                    twine upload dist/*
                                fi
                                
                                # Create GitHub release
                                curl -X POST \
                                    -H "Authorization: token ${GH_TOKEN}" \
                                    -H "Accept: application/vnd.github.v3+json" \
                                    https://api.github.com/repos/yourusername/py-math-lib/releases \
                                    -d '{
                                        "tag_name": "v${env.NEXT_VERSION}",
                                        "name": "v${env.NEXT_VERSION}",
                                        "body": "Release v${env.NEXT_VERSION}",
                                        "draft": false,
                                        "prerelease": ${env.RELEASE_CHANNEL == 'beta' ? 'true' : 'false'}
                                    }'
                            """
                        }
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo """
            ===== Build Successful =====
            Branch: ${env.TARGET_BRANCH}
            Commit: ${env.COMMIT_HASH}
            Version: ${env.CURRENT_VERSION}
            Status: SUCCESS
            ============================
            """
        }
        
        failure {
            echo """
            ===== Build Failed =====
            Branch: ${env.TARGET_BRANCH}
            Commit: ${env.COMMIT_HASH}
            Version: ${env.CURRENT_VERSION}
            Status: FAILURE
            =========================
            """
        }
        
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}

def calculateNextVersion(currentVersion, versionType) {
    def parts = currentVersion.tokenize('.')
    def major = parts[0] as Integer
    def minor = parts[1] as Integer
    def patch = parts[2] as Integer
    
    switch(versionType) {
        case 'major':
            return "${major + 1}.0.0"
        case 'minor':
            return "${major}.${minor + 1}.0"
        case 'patch':
            return "${major}.${minor}.${patch + 1}"
        default:
            return currentVersion
    }
}