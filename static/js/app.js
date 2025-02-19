
/*!
 * DAHA Template
 * Created on date: 1402/12/02
 * Built on date: 1403/04/13
 * 
 * View source code on GitHub: https://github.com/Mhadi-1382/daha-website-flask
*/

// SPLASH SCREEN
window.addEventListener("load", function() {
    setTimeout(() => {
        document.getElementById("splashScreen").remove("splash-screen");
    }, 1000);

    // STATUS INTERNET
    // if (navigator.onLine) {
    //     console.log("Online.");
    // } else {
    //     console.log("Offline.");
    
    //     setTimeout(() => {
    //         var AlertOfflineMode = document.getElementById("AlertOfflineMode");
    //         AlertOfflineMode.style.display = "flex";
    //         navigator.vibrate(200);
    //     }, 1000);
    // }
});


// STATUS INTERNET
var AlertOfflineMode = document.getElementById("AlertOfflineMode");
window.addEventListener("offline", function() {
    console.log("Offline.");
    
    setTimeout(() => {
        AlertOfflineMode.style.display = "flex";
        navigator.vibrate(200);
    }, 1000);
});
window.addEventListener("online", function() {
    console.log("Online.");
    
    AlertOfflineMode.style.display = "none";
});


// ALERTS
var alertDiplay = document.getElementById("alert-diplay");
setTimeout(() => {
    alertDiplay.style.display = "none";
}, 5000);

var modalAlertHomepage = document.getElementById("modalAlertHomepage");
var modalAlertHomepageTagh4Lenght = document.querySelector("#modalAlertHomepageTagh4Lenght");
var modalAlertHomepageTagPLenght = document.querySelector("#modalAlertHomepageTagPLenght");
function modalAlertHomepageFunc() {
    modalAlertHomepage.classList.toggle("modal-toggle");
    
    // sessionStorage.setItem("AlertDisplay", "None");
    document.cookie = "AlertDisplay= None; max-age= 259200"; // EXPIRE TIME 3 DAY
}
window.onload = function() {
    if (modalAlertHomepageTagPLenght.lenght == 0 | modalAlertHomepageTagh4Lenght.lenght == 0) {
        modalAlertHomepage.classList.remove("modal-toggle");
    } else {
        setTimeout(() => {
            if (document.cookie) {
                modalAlertHomepage.classList.remove("modal-toggle");
            } else {
                modalAlertHomepageFunc();
            }
        }, 2000);
    }
}


// NAVBAR MOBILE & MODALS
var navbarMobileSidebarRight = document.getElementById("navbarMobileSidebarRight");
var sidebarRight = document.getElementById("sidebarRight");
var actionButton = document.getElementById("actionButton");
var actionLinkClickToggle = document.getElementById("actionLinkClickToggle");
function toggleNavbarMobile() {
    navbarMobileSidebarRight.classList.toggle("navbar-mobile-toggle");
    sidebarRight.classList.toggle("sidebar-right-navbar-toggle");
    if (actionButton) {
        actionButton.classList.toggle("action-button-toggle");
        // sidebarRight.scrollTo({top: 0, behavior: "smooth"});
    } else {
    }

    actionLinkClickToggle.classList.toggle("action-link-click-toggle");
}

var dropdownUserAvatarWarpper = document.getElementById("dropdownUserAvatarWarpper");
var modalEditInfo = document.getElementById("modalEditInfo");
var modalStatusAd = document.getElementById("modalStatusAd");
var modalDeleteAccount = document.getElementById("modalDeleteAccount");
var modalHelpAdmin = document.getElementById("modalHelpAdmin");
function toggleDropdownUserAvatarWarpper() {
    dropdownUserAvatarWarpper.classList.toggle("dropdown-user-avatar-warpper-toggle");
}
function modalEditInfoFunc() {
    modalEditInfo.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
function modalStatusAdFunc() {
    modalStatusAd.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
function modalDeleteAccountFunc() {
    modalDeleteAccount.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
function modalHelpAdminFunc() {
    modalHelpAdmin.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}

// MODALS
var modalSupport = document.getElementById("modalSupport");
function modalSupportFunc() {
    modalSupport.classList.toggle("modal-toggle");
    
    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalAbout = document.getElementById("modalAbout");
function modalAboutFunc() {
    modalAbout.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalComment = document.getElementById("modalComment");
function modalCommentFunc() {
    modalComment.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalTicket = document.getElementById("modalTicket");
function modalTicketFunc() {
    modalTicket.classList.toggle("modal-toggle");
    modalSupport.classList.remove("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalVersionChanges = document.getElementById("modalVersionChanges");
function modalVersionChangesFunc() {
    modalVersionChanges.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalPrivacyPolicies = document.getElementById("modalPrivacyPolicies");
function modalPrivacyPoliciesFunc() {
    modalPrivacyPolicies.classList.toggle("modal-toggle");

    navbarMobileSidebarRight.classList.remove("navbar-mobile-toggle");
    sidebarRight.classList.remove("sidebar-right-navbar-toggle");
    actionLinkClickToggle.classList.remove("action-link-click-toggle");
}
var modalNotifications = document.getElementById("modalNotifications");
function modalNotificationsFunc() {
    modalNotifications.classList.toggle("modal-toggle");
}
var modalPossibilities1 = document.getElementById("modalPossibilities1");
function modalPossibilities1Func() {
    modalPossibilities1.classList.toggle("modal-toggle");
}
var modalPossibilities2 = document.getElementById("modalPossibilities2");
function modalPossibilities2Func() {
    modalPossibilities2.classList.toggle("modal-toggle");
}
var modalPossibilities3 = document.getElementById("modalPossibilities3");
function modalPossibilities3Func() {
    modalPossibilities3.classList.toggle("modal-toggle");
}
var modalPossibilities4 = document.getElementById("modalPossibilities4");
function modalPossibilities4Func() {
    modalPossibilities4.classList.toggle("modal-toggle");
}
var modalPossibilities5 = document.getElementById("modalPossibilities5");
function modalPossibilities5Func() {
    modalPossibilities5.classList.toggle("modal-toggle");
}
var modalPossibilities6 = document.getElementById("modalPossibilities6");
function modalPossibilities6Func() {
    modalPossibilities6.classList.toggle("modal-toggle");
}
var modalPossibilities7 = document.getElementById("modalPossibilities7");
function modalPossibilities7Func() {
    modalPossibilities7.classList.toggle("modal-toggle");
}
var modalTechnologist = document.getElementById("modalTechnologist");
function modalTechnologistFunc() {
    modalTechnologist.classList.toggle("modal-toggle");
}
var modalUploadFile = document.getElementById("modalUploadFile");
function modalUploadFileFunc() {
    modalUploadFile.classList.toggle("modal-toggle");
}
var modalDahaVoiceAssistant = document.getElementById("modalDahaVoiceAssistant");
function modalDahaVoiceAssistantFunc() {
    modalDahaVoiceAssistant.classList.toggle("modal-toggle");
}


// MAJORS CARD TOGGLE
var majorsCard1 = document.getElementById("majorsCard1");
var majorsCard2 = document.getElementById("majorsCard2");
function associateDegree() {
    majorsCard1.classList.toggle("majors-card-toggle");
    document.getElementById("associateDegreeBtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("associateDegreeBtnAngleUp").classList.toggle("btn-angle-up");
}
function undergraduate() {
    majorsCard2.classList.toggle("majors-card-toggle");
    document.getElementById("undergraduateBtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("undergraduateBtnAngleUp").classList.toggle("btn-angle-up");
}


// FORUMS CARD TOGGLE
var forumsCard1 = document.getElementById("forumsCard1");
var forumsCard2 = document.getElementById("forumsCard2");
var forumsCard3 = document.getElementById("forumsCard3");
var forumsCard4 = document.getElementById("forumsCard4");
function forums1() {
    forumsCard1.classList.toggle("majors-card-toggle");
    document.getElementById("forumsCard1BtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("forumsCard1BtnAngleUp").classList.toggle("btn-angle-up");
}
function forums2() {
    forumsCard2.classList.toggle("majors-card-toggle");
    document.getElementById("forumsCard2BtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("forumsCard2BtnAngleUp").classList.toggle("btn-angle-up");
}
function forums3() {
    forumsCard3.classList.toggle("majors-card-toggle");
    document.getElementById("forumsCard3BtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("forumsCard3BtnAngleUp").classList.toggle("btn-angle-up");
}
function forums4() {
    forumsCard4.classList.toggle("majors-card-toggle");
    document.getElementById("forumsCard4BtnAngleDown").classList.toggle("btn-angle-down");
    document.getElementById("forumsCard4BtnAngleUp").classList.toggle("btn-angle-up");
}


// MANAGEMENT FORMS
var emailTo = document.getElementById("emailTo_sendEmail");
function sendAllEmail() {
    emailTo.toggleAttribute("readonly");
    emailTo.classList.toggle("checkbox-not-allowed-disabled");
}

var eventSubmitLogin = document.getElementById("eventSubmitLogin");
var eventSubmitSingin = document.getElementById("eventSubmitSingin");
function eventSubmitLoginFunc() {
    eventSubmitLogin.value = "در حال بررسی...";
    setTimeout(() => {
        eventSubmitLogin.value = "ورود";
    }, 3000);
}
function eventSubmitSinginFunc() {
    eventSubmitSingin.value = "در حال بررسی...";
    setTimeout(() => {
        eventSubmitSingin.value = "ثبت نام";
    }, 3000);
}


// TOGGLE MODE
// var time = new Date();
var dahaLogoForDark = document.getElementById("dahaLogoForDark");
var dahaLogoForLight = document.getElementById("dahaLogoForLight");
var dahaLogoForDarkMobile = document.getElementById("dahaLogoForDarkMobile");
var dahaLogoForLightMobile = document.getElementById("dahaLogoForLightMobile");
var toggleModeTextMoon = document.getElementById("toggleModeTextMoon");
var toggleModeTextSun = document.getElementById("toggleModeTextSun");
function toggleThemeModeDark() {
    localStorage.setItem("ToggleThemeMode", "dark");

    document.body.classList.toggle("toggleMode");

    dahaLogoForDark.classList.toggle("btn-angle-up");
    dahaLogoForLight.classList.toggle("btn-angle-down");
    dahaLogoForDarkMobile.classList.toggle("btn-angle-up");
    dahaLogoForLightMobile.classList.toggle("btn-angle-down");
    
    toggleModeTextMoon.classList.add("btn-angle-down");
    toggleModeTextSun.classList.toggle("btn-angle-up");
}
function toggleThemeModelight() {
    localStorage.setItem("ToggleThemeMode", "light");

    document.body.classList.toggle("toggleMode");

    dahaLogoForDark.classList.toggle("btn-angle-up");
    dahaLogoForLight.classList.toggle("btn-angle-down");
    dahaLogoForDarkMobile.classList.toggle("btn-angle-up");
    dahaLogoForLightMobile.classList.toggle("btn-angle-down");
    
    toggleModeTextMoon.classList.toggle("btn-angle-down");
    toggleModeTextSun.classList.remove("btn-angle-up");
}
if (localStorage.getItem("ToggleThemeMode") == "dark") {
    document.body.classList.add("toggleMode");

    dahaLogoForDark.classList.toggle("btn-angle-up");
    dahaLogoForLight.classList.toggle("btn-angle-down");
    dahaLogoForDarkMobile.classList.toggle("btn-angle-up");
    dahaLogoForLightMobile.classList.toggle("btn-angle-down");
    
    toggleModeTextMoon.classList.add("btn-angle-down");
    toggleModeTextSun.classList.toggle("btn-angle-up");
} else if (localStorage.getItem("ToggleThemeMode") == "light") {
    document.body.classList.remove("toggleMode");
}


// GROUP TABS
var groupTabsContent1 = document.getElementById("groupTabsContent1");
var groupTabsContent2 = document.getElementById("groupTabsContent2");
var groupTabsActive1 = document.querySelector(".group-tabs .tab-actived1");
var groupTabsActive2 = document.querySelector(".group-tabs .tab-actived2");

function groupTabsFunc1() {
    groupTabsContent1.style.display = "flex";
    groupTabsContent2.style.display = "none";

    groupTabsActive1.classList.add("tab-active");
    groupTabsActive2.classList.remove("tab-active");
}
function groupTabsFunc2() {
    groupTabsContent1.style.display = "none";
    groupTabsContent2.style.display = "flex";

    groupTabsActive1.classList.remove("tab-active");
    groupTabsActive2.classList.add("tab-active");
}
