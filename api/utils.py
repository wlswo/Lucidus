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

  escaped_data = {k: custom_escape(v) if isinstance(v, str) else v for k, v in
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
        opacity: 0; /* 초기 상태에서 숨김 */
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
