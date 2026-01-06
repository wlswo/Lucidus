let currentMode = 'galaxy';


function setTextIfExist(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function setAttrIfExist(id, attr, value) {
    const el = document.getElementById(id);
    if (el) el.setAttribute(attr, value);
}

function generateLink() {
    let params = {
        name: document.getElementById('name').value,
        job: document.getElementById('job').value,
        company: document.getElementById('company').value,
        address: document.getElementById('address').value,
        about: document.getElementById('about').value,
        linkedin: document.getElementById('linkedin').value
    };

    let baseUrl = '';

    if (currentMode === 'galaxy') {
        params.theme = document.getElementById('theme').value;
        params.email = document.getElementById('email').value;
        baseUrl = 'https://criminal-vivyanne-lucidus-346ca075.koyeb.app/lucidus/card_v1?';
    } else {
        params.github = document.getElementById('github').value; // github 값 사용

        baseUrl = 'https://criminal-vivyanne-lucidus-346ca075.koyeb.app/lucidus/card_v2?';
    }

    const queryString = Object.keys(params)
        .map(key => key + '=' + encodeURIComponent(params[key]))
        .join('&');

    const fullUrl = baseUrl + queryString;

    const markdown = '![Lucidus](' + fullUrl + ')';
    const htmllink = '<object type="image/svg+xml" data=' + '"' + fullUrl + '"' + '></object>';
    const notion = fullUrl;

    document.getElementById('linkContainerMarkdown').textContent = markdown;
    document.getElementById('linkContainerHtml').textContent = htmllink;
    document.getElementById('linkContainerNotion').textContent = notion;
}

function updateSvg() {
    if (currentMode === 'galaxy') {
        const selectedThemeElement = document.querySelector('.theme-option.selected');
        const theme = selectedThemeElement ? selectedThemeElement.getAttribute('data-theme') : 'dark';

        const themes = {
            dark: ["#101010", "#2c3e50"],
            blue: ["#101010", "#29539B"],
            purple: ["#101010", "#923CB5"],
            cosmic: ["#0D324D", "#524053"],
            green: ["#213529", "#104b27"]
        };
        const [theme1, theme2] = themes[theme];

        const stop1 = document.getElementById('stopTheme1');
        const stop2 = document.getElementById('stopTheme2');
        if (stop1) stop1.setAttribute('style', 'stop-color:' + theme1 + '; stop-opacity:1');
        if (stop2) stop2.setAttribute('style', 'stop-color:' + theme2 + '; stop-opacity:1');
    }

    const name = document.getElementById('name').value;
    const job = document.getElementById('job').value;
    const company = document.getElementById('company').value;
    const address = document.getElementById('address').value;
    const about = document.getElementById('about').value;
    const linkedin = document.getElementById('linkedin').value;

    setTextIfExist('svgName', name);
    setTextIfExist('svgJob', job);
    setTextIfExist('svgCompany', company);
    setTextIfExist('svgAddress', address);
    setTextIfExist('svgAboutContent', about);
    setAttrIfExist('svgLinkedin', 'href', linkedin);

    setTextIfExist('svgName_metal', name);
    setTextIfExist('svgJob_metal', job);
    setTextIfExist('svgCompany_metal', company);
    setTextIfExist('svgAddress_metal', address);
    setTextIfExist('svgAboutContent_metal', about);
    setAttrIfExist('svgLinkedin_metal', 'href', linkedin);

    if (currentMode === 'galaxy') {
        const email = document.getElementById('email').value;
        setAttrIfExist('svgEmail', 'href', 'mailto:' + email);
    } else {
        const github = document.getElementById('github').value;
        setAttrIfExist('svgGithub_metal', 'xlink:href', 'https://github.com/' + github);
    }

    generateLink();
}

function switchMode(mode) {
    if (currentMode === mode) return;

    currentMode = mode;

    const btnGalaxy = document.getElementById('btnGalaxy');
    const btnMetal = document.getElementById('btnMetal');
    const themeGroup = document.getElementById('themeGroup');
    const emailGroup = document.getElementById('emailGroup');
    const githubGroup = document.getElementById('githubGroup');

    const galaxyPreview = document.getElementById('galaxy-preview');
    const metalPreview = document.getElementById('metal-preview');

    if (mode === 'galaxy') {
        btnGalaxy.classList.add('selected');
        btnMetal.classList.remove('selected');
        themeGroup.classList.remove('hidden');
        emailGroup.classList.remove('hidden');
        githubGroup.classList.add('hidden');

        galaxyPreview.classList.remove('hidden');
        metalPreview.classList.add('hidden');

    } else if (mode === 'metal') {
        btnGalaxy.classList.remove('selected');
        btnMetal.classList.add('selected');
        themeGroup.classList.add('hidden');
        emailGroup.classList.add('hidden');
        githubGroup.classList.remove('hidden');

        galaxyPreview.classList.add('hidden');
        metalPreview.classList.remove('hidden');
    }

    updateSvg();
    startSvgAnimation();
}

const inputs = document.querySelectorAll('#svgForm input, #svgForm select');
inputs.forEach(input => {
    input.addEventListener('input', updateSvg);
    input.addEventListener('change', updateSvg);
    input.addEventListener('keyup', updateSvg);
    input.addEventListener('blur', updateSvg);
});

function copyToClipboard(containerId) {
    const container = document.getElementById(containerId);
    const text = container.textContent.trim();

    navigator.clipboard.writeText(text).then(() => {
        const button = container.parentElement.querySelector(".copy-btn");
        const originalText = button.textContent;

        button.textContent = "COPIED!";
        button.classList.add("copied");

        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove("copied");
        }, 1500);
    }).catch(err => {
        console.error("copy fail: ", err);
    });
}

function startSvgAnimation() {
    const wrapperId = (currentMode === 'galaxy') ? 'galaxy-preview' : 'metal-preview';
    const wrapper = document.getElementById(wrapperId);

    if (!wrapper) return;

    const oldSvg = wrapper.querySelector('svg');
    if (oldSvg) {
        const newSvg = oldSvg.cloneNode(true);
        oldSvg.parentNode.replaceChild(newSvg, oldSvg);
    }
}

document.querySelectorAll('.theme-option').forEach(option => {
    option.addEventListener('click', function () {
        document.querySelectorAll('.theme-option').forEach(opt => opt.classList.remove('selected'));
        this.classList.add('selected');
        document.getElementById('theme').value = this.getAttribute('data-theme');
        updateSvg();
    });
});

document.getElementById('btnGalaxy').addEventListener('click', () => switchMode('galaxy'));
document.getElementById('btnMetal').addEventListener('click', () => switchMode('metal'));

document.getElementById('restartAnimation').addEventListener('click', function () {
    startSvgAnimation();
});

window.addEventListener('DOMContentLoaded', () => {
    updateSvg();
    startSvgAnimation();
});