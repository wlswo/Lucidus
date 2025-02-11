function generateLink() {
        const params = {
            theme: document.getElementById('theme').value,
            name: document.getElementById('name').value,
            job: document.getElementById('job').value,
            company: document.getElementById('company').value,
            address: document.getElementById('address').value,
            about: document.getElementById('about').value,
            email: document.getElementById('email').value,
            linkedin: document.getElementById('linkedin').value
        };

        const queryString = Object.keys(params)
            .map(key => key + '=' + encodeURIComponent(params[key]))
            .join('&');

        const baseUrl = 'https://criminal-vivyanne-lucidus-346ca075.koyeb.app/lucidus/card_v1?';
        const fullUrl = baseUrl + queryString;

        const markdown = '![Lucidus](' + fullUrl + ')';
        const htmllink = '<object type="image/svg+xml" data=' + '"' + fullUrl + '"' + '></object>';
        const notion = fullUrl;

        document.getElementById('linkContainerMarkdown').textContent = markdown;
        document.getElementById('linkContainerHtml').textContent = htmllink;
        document.getElementById('linkContainerNotion').textContent = notion;
    }

    function updateSvg() {
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

        const name = document.getElementById('name').value;
        const job = document.getElementById('job').value;
        const company = document.getElementById('company').value;
        const address = document.getElementById('address').value;
        const about = document.getElementById('about').value;
        const email = document.getElementById('email').value;
        const linkedin = document.getElementById('linkedin').value;

        document.getElementById('stopTheme1').setAttribute('style',
            'stop-color:' + theme1 + '; stop-opacity:1');
        document.getElementById('stopTheme2').setAttribute('style',
            'stop-color:' + theme2 + '; stop-opacity:1');

        document.getElementById('svgName').textContent = name;
        document.getElementById('svgJob').textContent = job;
        document.getElementById('svgCompany').textContent = company;
        document.getElementById('svgAddress').textContent = address;
        document.getElementById('svgAboutContent').textContent = about;

        document.getElementById('svgEmail').setAttribute('href', 'mailto:' + email);
        document.getElementById('svgLinkedin').setAttribute('href', linkedin);

        generateLink();
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
        const svgContainer = document.getElementById('svgPreview');
        const oldSvg = svgContainer.querySelector('svg');
        if (oldSvg) {
            svgContainer.classList.remove('no-animation');
            const newSvg = oldSvg.cloneNode(true);
            svgContainer.replaceChild(newSvg, oldSvg);
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

    document.getElementById('restartAnimation').addEventListener('click', function () {
        startSvgAnimation();
    });

    window.addEventListener('DOMContentLoaded', () => {
        updateSvg();
        startSvgAnimation();
    });