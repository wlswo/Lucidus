from string import Template
from xml.sax.saxutils import escape

from fastapi import HTTPException

from api import constants


def custom_escape(text: str) -> str:
    if not isinstance(text, str):
        return text
    # Default XML Escape Character : &, <, >, @ Replace
    escaped = escape(text).replace("@", "&#64;")

    return escaped


def validation(data: dict):
    """
    Data validation function
    - Limits field length to 80 characters
    """
    MAX_LENGTH = 80

    for field, value in data.items():

        # Check if the field value exceeds 80 characters
        if len(value) > MAX_LENGTH:
            raise HTTPException(status_code=400,
                                detail=f"'{field}' field exceeds the maximum length of 80 characters.")


def get_theme(theme):
    return constants.theme.get(theme.strip().lower(), constants.theme["dark"])


def generate_card(data: dict):
    validation(data)

    escaped_data = {key: custom_escape(value) if isinstance(value, str) else value for key, value in
                    data.items()}
    theme = get_theme(escaped_data.get("theme", "dark"))

    svg = Template('''
    <!DOCTYPE svg PUBLIC
        "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" gradientTransform="rotate(45)">
      <stop offset="0%" style="stop-color:$theme1; stop-opacity:1" />
      <stop offset="100%" style="stop-color:$theme2; stop-opacity:1" />
    </linearGradient>
    
    <style>

      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      
      @keyframes drawBoxPart1 {
        0% { stroke-dasharray: 0 40; }
        100% { stroke-dasharray: 40 0; }
      }
      
      @keyframes drawBoxPart2 {
        0% { stroke-dasharray: 0 40; }
        100% { stroke-dasharray: 40 0; }
      }
      
      @keyframes drawCheck {
        0% { stroke-dasharray: 0 30; }
        100% { stroke-dasharray: 30 0; }
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @keyframes twinkle {
        0% { opacity: 0.2; }
        50% { opacity: 1; }
        100% { opacity: 0.2; }
      }
      
      .twinkling-star {
        fill: white;
        opacity: 0.2;
        animation: twinkle 2s infinite alternate;
      }
      
      text {
        font-family: "Open Sans", sans-serif;
        fill: white;
        font-size: 22px;
        opacity: 0;
        animation: fadeIn 1s ease-in-out forwards;
        dominant-baseline: middle;
      }
      
      text.name {
        font-size: 30px;
        font-weight: bold;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 0.6s;
      }

      text.job {
        font-size: 18px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1s;
      }

      text.company {
        font-size: 18px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.2s;
      }

      text.address {
        fill: #777777;
        font-size: 15px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.4s;
      }

      text.about {
        fill: white;
        font-size: 22px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.8s;
      }

      text.about-content {
        fill: #979696;
        font-size: 15px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.9s;
      }
          
      .address-icon { 
        fill: #777777;
        opacity: 0;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.5s;
      }

      .icon line {
        stroke: white;
        stroke-width: 1.5;
        fill: none;
      }
      
      .icon .top-left {
        stroke-dasharray: 40;
        stroke-dashoffset: 40;
        animation-delay: 3s;
        animation: drawBoxPart1 1s forwards; animation-delay: 2.6s;
      }
      
      .icon .bottom-right {
        stroke-dasharray: 40;
        stroke-dashoffset: 40;
        animation: drawBoxPart2 1s forwards; animation-delay: 2.8s;
      }
      
      .check {
        stroke: white;
        stroke-width: 1.5;
        fill: none;
        stroke-dasharray: 30;
        stroke-dashoffset: 30;
        animation: drawCheck 0.5s forwards; animation-delay: 3s;
      }

      .icon:hover line, .icon:hover .check {
        stroke: #3498db;
        transition: stroke 0.3s ease;
        cursor: pointer;
      }

      .linkedin {
        opacity: 0;
        animation: fadeIn 1.5s ease-in-out forwards; animation-delay: 2s;
      }

    </style>
  </defs>
  
  <rect x="10" y="10" width="400" height="230" rx="0" ry="0" fill="url(#grad)" />

  <g id="stars">
    <circle class="twinkling-star" cx="50" cy="30" r="1.1" style="animation-delay: 0s;"/>
    <circle class="twinkling-star" cx="300" cy="50" r="1.3" style="animation-delay: 1s;"/>
    <circle class="twinkling-star" cx="290" cy="30" r="1" style="animation-delay: 2s;"/>
    <circle class="twinkling-star" cx="240" cy="100" r="1.4" style="animation-delay: 3s;"/>
    <circle class="twinkling-star" cx="370" cy="140" r="1.5" style="animation-delay: 4s;"/>
  </g>

  <text class="name" x="50" y="60">$name</text>

  <text class="job" x="50" y="90">$job</text>
  <text class="company" x="50" y="115">$company</text>
  <g transform="translate(45, 135)">
    <text class="address" x="30" y="13">$address</text>
    <path class="address-icon" d="M12 2C8.686 2 6 4.686 6 8C6 12.627 12 21 12 21C12 21 18 12.627 18 8C18 4.686 15.314 2 12 2zM12 10C10.895 10 10 9.105 10 8C10 6.895 10.895 6 12 6C13.105 6 14 6.895 14 8C14 9.105 13.105 10 12 10z" />
  </g>

  <text class="about" x="50" y="190">About Me</text>
  <text class="about-content" x="50" y="210">$about.</text>

  <a href="mailto:$email">
    <g class="icon" transform="translate(377, 20) rotate(45)">
      <rect x="-5" y="-5" width="30" height="30" fill="transparent" pointer-events="all" />

      <line class="top-left" x1="-0.5" y1="0.5" x2="20.5" y2="0.5" />
      <line class="top-left" x1="0" y1="0" x2="0" y2="15" />
      <line class="bottom-right" x1="-0.5" y1="14.5" x2="20.5" y2="14.5" />
      <line class="bottom-right" x1="20" y1="0" x2="20" y2="15" />
      
      <polyline class="check" points="0.5,0.5 10,10 19.5,1" />
    </g>
  </a>

  <a href="$linkedin">
    <g class="linkedin" transform="translate(340, 180) scale(1)">
      <path fill="#c37d16" d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5V37z"></path>
      <path fill="#FFF" d="M12 19H17V36H12zM14.485 17h-.028C12.965 17 12 15.888 12 14.499 12 13.08 12.995 12 14.514 12c1.521 0 2.458 1.08 2.486 2.499C17 15.887 16.035 17 14.485 17zM36 36h-5v-9.099c0-2.198-1.225-3.698-3.192-3.698-1.501 0-2.313 1.012-2.707 1.99C24.957 25.543 25 26.511 25 27v9h-5V19h5v2.616C25.721 20.5 26.85 19 29.738 19c3.578 0 6.261 2.25 6.261 7.274L36 36 36 36z"></path>
    </g>
  </a>
</svg>''').safe_substitute(
        theme1=theme[0],
        theme2=theme[1],
        name=escaped_data.get("name"),
        job=escaped_data.get("job"),
        company=escaped_data.get("company"),
        address=escaped_data.get("address"),
        about=escaped_data.get("about"),
        email=escaped_data.get("email"),
        linkedin=escaped_data.get("linkedin")
    )

    return svg


def generate_card_v2(data: dict):
    validation(data)

    escaped_data = {key: custom_escape(value) if isinstance(value, str) else value for key, value in
                    data.items()}

    svg = Template('''
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="cardClip">
      <rect x="10" y="10" width="380" height="230" rx="15" ry="15" />
    </clipPath>

    <linearGradient id="metalBase" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f1012" />
      <stop offset="40%" stop-color="#3b4047" />
      <stop offset="100%" stop-color="#0a0a0a" />
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="40%" r="60%" fx="50%" fy="40%">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.15" />
      <stop offset="60%" stop-color="#3b82f6" stop-opacity="0" />
    </radialGradient>

    <linearGradient id="sidebarMetalGradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#2e2e2e" />
        <stop offset="100%" stop-color="#000000" />
    </linearGradient>

    <linearGradient id="shineGradient" x1="0" y1="0" x2="0" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="rotate(30)">
      <stop offset="0%" stop-color="#b5b5b5" />
      <stop offset="35%" stop-color="#b5b5b5" />
      <stop offset="50%" stop-color="#ffffff" /> 
      <stop offset="65%" stop-color="#b5b5b5" />
      <stop offset="100%" stop-color="#b5b5b5" />
      <animate attributeName="x1" from="-600" to="1000" dur="4s" repeatCount="indefinite" />
      <animate attributeName="x2" from="-400" to="1200" dur="4s" repeatCount="indefinite" />
    </linearGradient>

    <filter id="neon-glow" filterUnits="userSpaceOnUse" x="-500" y="-500" width="1500" height="1500">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    
    <style>
      @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
      @keyframes fadeInSimple { from { opacity: 0; } to { opacity: 1; } }
      
      text {
        font-family: "Open Sans", sans-serif;
        fill: #c7c5c5; 
        font-size: 14px;
        opacity: 0;
        animation: fadeIn 1s ease-in-out forwards;
        dominant-baseline: hanging;
        text-anchor: start;
      }
      
      text.name {
        font-size: 28px;
        font-weight: bold;
        fill: url(#shineGradient); 
        animation-delay: 0.6s;
        dominant-baseline: auto;
      }

      text.job { font-size: 16px; font-weight: 1; animation-delay: 1s; }
      text.company { font-size: 16px; font-weight: 1; animation-delay: 1.2s; }
      text.address { font-size: 14px; font-weight: 1; animation-delay: 1.4s; }
      text.about { font-size: 18px; font-weight: bold; animation-delay: 1.8s; dominant-baseline: auto; }
      text.about-content { font-size: 14px; font-weight: 1; animation-delay: 1.9s; fill: #999; }
          
      .address-icon { fill: #b5b5b5; opacity: 0; animation: fadeInSimple 0.5s ease-in-out forwards; animation-delay: 1.5s; }
      .linkedin { opacity: 0; animation: fadeInSimple 1.5s ease-in-out forwards; animation-delay: 2s; }

      .link-wrapper:hover .hover-target {
        filter: url(#neon-glow);
        stroke: #e0f2ff; 
      }
      .hover-target path {
        transition: stroke 0.3s ease;
      }
    </style>
  </defs>
  
  <rect x="10" y="10" width="380" height="230" rx="15" ry="15" fill="url(#metalBase)" />
  
  <rect x="330" y="0" width="90" height="250" fill="url(#sidebarMetalGradient)" opacity="0.9" clip-path="url(#cardClip)" />

  <g transform="translate(50, 55)">
    <text class="name" x="0" y="10">$name</text>
    <text class="job" x="0" y="35">$job</text>
    <text class="company" x="0" y="55">$company</text>
    <g transform="translate(0, 90)">
        <path class="address-icon" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" transform="translate(-5, -4.5) scale(0.8)"/>
        <text class="address" x="18" y="0">$address</text>
    </g>
  </g>

  <g transform="translate(50, 190)">
    <text class="about" x="0" y="0">About Me</text>
    <text class="about-content" x="0" y="10">$about</text>
  </g>

  <a href="https://linkedin.com/in/johndoe">
    <g class="linkedin" transform="translate(340, 190) scale(0.8)">
      <path fill="#c37d16" d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5V37z"></path>
      <path fill="#FFF" d="M12 19H17V36H12zM14.485 17h-.028C12.965 17 12 15.888 12 14.499 12 13.08 12.995 12 14.514 12c1.521 0 2.458 1.08 2.486 2.499C17 15.887 16.035 17 14.485 17zM36 36h-5v-9.099c0-2.198-1.225-3.698-3.192-3.698-1.501 0-2.313 1.012-2.707 1.99C24.957 25.543 25 26.511 25 27v9h-5V19h5v2.616C25.721 20.5 26.85 19 29.738 19c3.578 0 6.261 2.25 6.261 7.274L36 36 36 36z"></path>
    </g>
  </a>

  <g transform="translate(333, 22) scale(0.10)">
  <a xlink:href="$github" target="_blank" style="cursor: pointer;" class="link-wrapper">
  <g class="hover-target"><path d="M256 70.7c-102.6 0-185.9 83.2-185.9 185.9 0 82.1 53.3 151.8 127.1 176.4 9.3 1.7 12.3-4 12.3-8.9V389.4c-51.7 11.3-62.5-21.9-62.5-21.9 -8.4-21.5-20.6-27.2-20.6-27.2 -16.9-11.5 1.3-11.3 1.3-11.3 18.7 1.3 28.5 19.2 28.5 19.2 16.6 28.4 43.5 20.2 54.1 15.4 1.7-12 6.5-20.2 11.8-24.9 -41.3-4.7-84.7-20.6-84.7-91.9 0-20.3 7.3-36.9 19.2-49.9 -1.9-4.7-8.3-23.6 1.8-49.2 0 0 15.6-5 51.1 19.1 14.8-4.1 30.7-6.2 46.5-6.3 15.8 0.1 31.7 2.1 46.6 6.3 35.5-24 51.1-19.1 51.1-19.1 10.1 25.6 3.8 44.5 1.8 49.2 11.9 13 19.1 29.6 19.1 49.9 0 71.4-43.5 87.1-84.9 91.7 6.7 5.8 12.8 17.1 12.8 34.4 0 24.9 0 44.9 0 51 0 4.9 3 10.7 12.4 8.9 73.8-24.6 127-94.3 127-176.4C441.9 153.9 358.6 70.7 256 70.7z"
          fill="transparent"
          stroke="#ADD8E6"
          stroke-width="15"
          stroke-dasharray="5000"
          stroke-dashoffset="5000">

          <animate attributeName="stroke-dashoffset" from="5000" to="0" begin="2.4s" dur="4s" fill="freeze" />
    </path>
  </g>
</a>
  </g>
</svg>
    ''').safe_substitute(
        name=escaped_data.get("name"),
        job=escaped_data.get("job"),
        company=escaped_data.get("company"),
        address=escaped_data.get("address"),
        about=escaped_data.get("about"),
        github=escaped_data.get("github"),
        linkedin=escaped_data.get("linkedin")
    )

    return svg
