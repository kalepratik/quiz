@echo off
echo ========================================
echo   dbt Certification Quiz - GitHub Deploy
echo ========================================
echo.

echo This script will help you deploy your project to GitHub.
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo Git is installed. Proceeding...
echo.

REM Check if we're in a Git repository
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add all files
echo Adding files to Git...
git add .

REM Check if there are changes to commit
git diff --cached --quiet
if errorlevel 1 (
    echo Committing changes...
    git commit -m "Initial commit: dbt Certification Quiz Application"
    echo.
) else (
    echo No changes to commit.
    echo.
)

REM Check if remote origin exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo   GitHub Repository Setup Required
    echo ========================================
    echo.
    echo Please follow these steps:
    echo.
    echo 1. Go to https://github.com
    echo 2. Click the "+" icon and select "New repository"
    echo 3. Name it: dbt-certification-quiz
    echo 4. Make it Public (recommended)
    echo 5. DO NOT initialize with README (we already have one)
    echo 6. Click "Create repository"
    echo.
    echo After creating the repository, GitHub will show you commands.
    echo Copy the URL of your repository (it will look like):
    echo https://github.com/YOUR_USERNAME/dbt-certification-quiz.git
    echo.
    set /p REPO_URL="Enter your GitHub repository URL: "
    
    if not defined REPO_URL (
        echo No URL provided. Exiting...
        pause
        exit /b 1
    )
    
    echo Adding remote origin...
    git remote add origin %REPO_URL%
    echo.
)

REM Set main branch and push
echo Setting main branch and pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Failed to push to GitHub.
    echo This might be because:
    echo - You haven't created the repository yet
    echo - You need to authenticate with GitHub
    echo - The repository URL is incorrect
    echo.
    echo Please check your GitHub repository and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! Your project is on GitHub!
echo ========================================
echo.
echo Your repository is now available at:
git remote get-url origin
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Share it with the dbt community
echo 3. Consider adding more questions
echo 4. Create releases for major updates
echo.
echo Happy coding! 🚀
echo.
pause
