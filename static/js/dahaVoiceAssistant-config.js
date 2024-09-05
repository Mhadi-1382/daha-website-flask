
// 12 command.

var queryLive = document.getElementById('queryLive');
var buttonMicrophoneClicked = document.getElementById('buttonMicrophoneClicked');
var indicatorMicrophoneClicked = document.getElementById('indicatorMicrophoneClicked');

function majors() {
    window.open('/pages/majors/');
}
function sites() {
    window.open('/pages/sites/');
}
function food_reservation() {
    window.open('/pages/food-reservation/');
}
function bustan() {
    window.open('https://bustan.tvu.ac.ir/');
}
function forums() {
    window.open('/pages/forums/');
}
function technologist() {
    window.open('/pages/technologist/');
}
function events() {
    window.open('/pages/events/');
}
function map_allameh_hassanzadeh_amoli() {
    window.open('https://www.google.com/maps/place/Allameh+Hassanzadeh+Amoli/@36.5186425,52.3299411,15z/data=!4m6!3m5!1s0x3f8fa2258572fd69:0xf703fd230fa02746!8m2!3d36.5186425!4d52.3299411!16s%2Fg%2F11cn0qdb5q?entry=ttu');
}
function publishers() {
    window.open('/pages/publishers/');
}
function edit_info() {
    modalDahaVoiceAssistantFunc();
    modalEditInfoFunc();
}
function toggleTheme() {
    toggleThemeModeDark();
}

if (annyang) {
    const command1 = {
        'رشته‌ها': () => { majors(); }
    };
    const command2 = {
        'سامانه‌ها': () => { sites(); }
    };
    const command3 = {
        'رزرو غذا': () => { food_reservation(); }
    };
    const command4 = {
        'بوستان': () => { bustan(); }
    };
    const command5 = {
        'انجمن‌ها': () => { forums(); }
    };
    const command6 = {
        'فناور': () => { technologist(); }
    };
    const command7 = {
        'رویدادها': () => { events(); }
    };
    const command8 = {
        'نقشه دانشکده': () => { map_allameh_hassanzadeh_amoli(); }
    };
    const command9 = {
        'انتشارات': () => { publishers(); }
    };
    const command10 = {
        'ویرایش اطلاعات': () => { edit_info(); }
    };
    const command11 = {
        'حالت شب': () => { toggleTheme(); }
    };
    const command12 = {
        'حالت روز': () => { toggleTheme(); }
    };

    annyang.addCommands(command1);
    annyang.addCommands(command2);
    annyang.addCommands(command3);
    annyang.addCommands(command4);
    annyang.addCommands(command5);
    annyang.addCommands(command6);
    annyang.addCommands(command7);
    annyang.addCommands(command8);
    annyang.addCommands(command9);
    annyang.addCommands(command10);
    annyang.addCommands(command11);
    annyang.addCommands(command12);

    annyang.setLanguage('fa-IR');
    annyang.debug();

    annyang.addCallback('resultMatch', function(userSaid, commandText) {
        queryLive.innerHTML = userSaid;
        console.log(commandText);
    });
    annyang.addCallback('resultNoMatch', function(userSaid) {
        // queryLive.innerHTML = 'متوجه نشدم! لطفا دوباره بگو';
        queryLive.innerHTML = userSaid[0];
    });

    // annyang.start({ autoRestart: false, continuous: false });
}

function startAnnyang() {
    annyang.resume();
    buttonMicrophoneClicked.onclick = function() {
        annyang.pause();
        buttonMicrophoneClicked.classList.toggle('button-microphone-clicked-animation-toggle')
    }
}
