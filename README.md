
# daha-website-flask

![GitHub Repo Size](https://img.shields.io/github/repo-size/Mhadi-1382/daha-website-flask
)
![GitHub Stars](https://img.shields.io/github/stars/Mhadi-1382/daha-website-flask
)
![GitHub Forks](https://img.shields.io/github/forks/Mhadi-1382/daha-website-flask
)

<br>

<img src="https://github.com/Mhadi-1382/daha-website-flask/blob/master/static/media/images/icon.svg" alt="daha-website-flask" width="80">

**Daha, quick access to all university facilities.**

With the Daha application, you can easily do things related to your university;
Things like downloading lesson charts, important sites, receiving news and issues related to the university and students as notifications and emails, receiving textbooks, introducing or promoting business cards, and many other attractive features.

<br>

## Installation
You can install project dependencies like this:
```
pip install -r requirements.txt
```

## Screenshots
<img src="https://github.com/Mhadi-1382/daha-website-flask/blob/master/static/media/imgs/screenshots/shot-1.jpg" alt="daha-website-flask">

## Version changes
> **Version (1.8.2):**
- The ability to execute defined commands by voice (Daha voice assistant, BETA stage - 12 commands).
- Added the ability to close the menu by touching the screen with background blur.
- Added the ability to register and log in to the user account (authentication for logging in with a security key; 4 to 6 digits) for professors and authentication of dashboard information with national code and session.
- The dedicated dashboard of professors (uploading pamphlets, sending notifications) and the possibility of managing professors and their information in the administrator's dashboard.
- Adding the teachers' announcements section on the main page.
- Create an update page and redirect all routes to this page on the server.
- Fixing the Session problem.
- The ability to view version changes by clicking on the version number.
- Adding notifications section and displaying them.
- Adding the ability to manage professors, and display splash as a flasher; In root mode (DAHA CLI v1.1.0).
- Creation of APIs system (v1.0.0) and full documentation page and registration of developers along with web service test rules and... User authentication with password (10 digits) sent by the administrator, ability to manage, confirm and send password by administrator (automation by button).
- Web services include 3 sections: Users web service, Users Email web service, Ads web service.
- Added the ability to register ticket responses in a modal way (automation by button).
- Added the ability to register, reject, confirm and pay, finish displaying ads on the report page (automation by button).
- Changing the ad status in different stages, adding categories in the technology section.
- Added the ability to link in advertisements and professors' announcements as ID for cards.
- Added the ability to select a package in the ad registration stage by the user and display the amount at the same time.
- Fixed the security problem in the section of sending requests with the POST method.
- Added the ability to record additional information in the information editing section as a tab (contact number, national code, date of birth, field of study, education, job, interests).
- Bug fixes and minor changes.

 > **Version (1.0.0):**
- Registration and login based on access level.
- (modal) registration conditions or rules.
- Password recovery.
- Email sending (automatic); Welcome after registration, forgot password, registration and confirmation of ad, delete account for user.
- Report cards on the admin page.
- (Modal form) Loading the brochure.
- (modal form) add system.
- (modal form) add event.
- (modal form) add ad.
- (modal form) sending email to a user or group sending (Checkbox).
- (modal form) sending notifications to users (Pusher Web service).
- (modal form) sending a notification or message on the main page and managing it.
- (modal form) file upload.
- (modal) existence of important points in some modals.
- Ability to view and manage files.
- Ability to delete user, ad, file, etc. on the pages related to the report.
- The possibility of deleting, rejecting the request, and ending the ad display on the ad report page.
- There are three levels of access to information; Red status (full administrator: management of administrators and server..), green (administrator: management of dashboards and professors..), blue (user: first class (professors, or with high access) and second class (students, or with low access) )).
- Changing the color of the avatar based on the alphabet and displaying the first letter of the username.
- (modal) possibility to edit information.
- (Modal) Display the history of ads sent.
- With dark and light themes, save in LocalStorage.
- (Modal) has admin help (only in admin dashboard).
- Has a landing page to download and receive more information from the web app.
- (modal form) possibility to send comments.
- (modal) has an About Us section.
- (modal) has a support section; Send email, (modal form) send ticket, send message in IT.
- The possibility of exiting the user account.
- has a section; Courses, systems, food reservation, gardens, associations, technology, events, faculty map, publications on the main page.
- Ability to detect offline or no internet access.
- Responsive ability.
- Minimal and simple design.
- use of fonts; Dana (text) and Asom font (icon).
- Using flat and colored icons on the main page.
- Includes robots.txt and sitemap.xml file.
- use of; Session to manage user sessions (30 days expiration), Cookie to manage notification display (3 days expiration), LocalStorage to manage dark and light web app modes.
- The possibility of installing and using the web app on the browser (dahauni.ir), Android (APK), Windows (EXE) and also the feature (PWA) that can be run on all devices.

## Licence
This project is <a href="https://github.com/Mhadi-1382/daha-website-flask/blob/master/LICENSE">MIT<a/> licenced.
