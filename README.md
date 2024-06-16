# Install instruction
1. Install pyenv
```
brew install pyenv
brew update
brew upgrade pyenv
pyenv install <python version>
```
2. Install python and set global/local python version
```
pyenv install 3.9.11
pyenv global 3.9.11
pyenv local 3.9.11
pyenv virtualenv 3.9.11 .venv
```
3. Activate and deactivate .venv
```
pyenv shell 3.9.11
python -m venv .venv
```
4. Install pipenv
```
pip install pipenv
pipenv activate
pipenv deactivate

```
5. Git repo
```
git clone
git config --global credential.helper store
```
6. Setup project
```
pipenv install
./deploy.sh
```

7. Configure project
`copy .env-template .env`

# install apps and packages
```
1. install packages
    pipenv install

2. install Node    
    # download and install Node.js
    `brew install node@20`
    # verifies the right Node.js version is in the environment
    `node -v` # should print `v20.13.1`
    # verifies the right NPM version is in the environment
    `npm -v` # should print `10.5.2` 
    # If you need to have node@20 first in your PATH, run:
    `echo 'export PATH="/usr/local/opt/node@20/bin:$PATH"' >> /Users/name/.bash_profile`
    ref. https://appium.io/docs/en/latest/quickstart/

3. install appium (follow guide from this link) and Check to make sure appium is installed, run this cmd on terminal
    appium
    
    eg.
    [Appium] Welcome to Appium v1.21.0
    [Appium] Appium REST http interface listener started on 0.0.0.0:4723
    
    Sample code: https://appium.io/docs/en/latest/quickstart/test-py/
    To upgrade `npm update -g appium`
    Download Appium Server: https://github.com/appium/appium-desktop/releases
    Download Appium Inspector: https://appium.github.io/appium-inspector/latest/quickstart/installation/#macos
    Install driver: `xcodebuild -version && sw_vers && rm -rf ~/.appium && npm install -g appium@next && appium driver install xcuitest && appium --allow-cors`
    
    Real Device Config: 
        https://appium.github.io/appium-xcuitest-driver/latest/preparation/real-device-config/
        Enable Developer Mode: https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device
        `appium driver run xcuitest open-wda`
        It is possible to build WebDriverAgentRunner for a generic iOS/iPadOS/tvOS device, and install the generated .app package to a real device.
        # iOS/iPadOS
        `xcodebuild clean build-for-testing -project WebDriverAgentRunner.xcodeproj -derivedDataPath appium_wda_ios -scheme WebDriverAgentRunner -destination generic/platform=iOS CODE_SIGNING_ALLOWED=YES`
    
4. install Android Studio and Emulator (for Android)
    ref. https://www.alphr.com/run-android-emulator/
    Install driver: `xcodebuild -version && sw_vers && rm -rf ~/.appium && npm install -g appium@next && appium driver install uiautomator2 && appium --allow-cors`
    start `emulator -avd <device-name>`, e.g `emulator -avd emulator-5554 --allow-cors`
    stop `adb -s emulator-5554 emu kill` or `adb devices | grep emulator | cut -f1 | while read line; do adb -s $line emu kill; done`

5. install iOS simuator (only for MAC OS)
    ref. https://www.kindacode.com/article/how-to-install-an-ios-simulator-in-xcode/
    view devices list `xcrun simctl list` 
    Now you should be able to use simctl to install and launch commands.
        xcrun simctl install <YOUR-DEVICE-ID> <PATH-TO-APPLICATION-BUNDLE>
        xcrun simctl launch <YOUR-DEVICE-ID> <BUNDLE-ID-OF-APP-BUNDLE>
    start `open -a Simulator`, start with specific identifier `open -a Simulator --args -CurrentDeviceUDID <YOUR-DEVICE-ID>`
    stop `killall Simulator`
    
6. install for aq with iOS reeal device
    This allows Appium to complete certain operations since the Apple apps do not easily enable programmatic use.
    `pipenv install libimobiledevice`
    This package will allow you to transfer iOS apps onto your device
    `pipenv install ios-deploy`  # pipenv uninstall ios-deploy, then brew install ios-deploy if RuntimeError: Failed to lock Pipfile.lock!
    Appium will automatically build the WDA app. Since WDA requires a dependency manager for iOS called Carthage, we will need to install this to enable the WDA bootstrap process.
    `pipenv install carthage`    # pipenv uninstall ios-deploy, then brew install carthage if RuntimeError: Failed to lock Pipfile.lock!
    ref. https://medium.com/@abhaykhs/using-appium-to-run-ios-tests-on-real-devices-fabd9850a06a
```

# Config for execution
```
1. copy config_example.py to config_local.py (if not exist yet)

2. Config for run on release (Note: your local machine must allowed connect with release env)
    change this variable with your user release=f"{username}@{ip_release}" 
    ex : release="trang@35.187.235.57"
    
    set variable environment='local'
   
3. Config for run on aqa-appium server with Docker (Note: you must allowed connect to aqa-appium sever)
    set variable environment='docker' and dri='docker'
    change container_atlas and container_postgres variables with your container name
    ex. container_atlas="gc_atlas_tt" and container_postgres="gc_postgres_tt"
```

# Execute the TestCase

1. Run with release env 
    a. Change variables on config file for running with release env
    b. start docker `docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm seleniarm/standalone-chromium:4.0.0-beta-1-20210215`
    c. view docker container via VNC with `localhost:5900`
    d. Run testcase :
        All testcase are on this path : aQA/android/src
        Chose product you want to run the testcase and run file : run_{product}.sh file from this product folder

2. Run with Docker on aqa-appium server
    a. Connect to aqa-appium sever : ex. ssh {username}@34.87.182.148
    b. Go to assurance repo : cd /opt/gigacover/assurance
    c. Change variables on config file for running with aqa-appium server
    d. Start selenium and emulator containers
        docker start selenium-container
        docker start android-container
    e. Make sure emulator has start successfuly
        go to : http://34.87.182.148:6080/
        Should see emulator if android-container has start successfuly
        Restart container if not see emulator and re-check again: docker restart android-container
    f. Run testcase (Make sure you are at /opt/gigacover/assurance)
        ./cron/daily_cronjob_aqa/aqa_daily.sh
