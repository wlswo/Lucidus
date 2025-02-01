def generate_card():
  svg = '''
    <!DOCTYPE svg PUBLIC
        "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 선형 그라디언트 정의: 배경 색상 설정 -->
    <linearGradient id="grad" gradientTransform="rotate(45)">
      <stop offset="0%" style="stop-color:#101010; stop-opacity:1" /> <!-- 시작 색상 -->
      <stop offset="100%" style="stop-color:#2c3e50; stop-opacity:1" /> <!-- 끝 색상 -->
    </linearGradient>
    
    <!-- CSS 스타일 및 애니메이션 정의 -->
    <style>

      /* 텍스트가 서서히 나타나는 애니메이션 */
      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); } /* 처음 투명 상태, 아래 위치 */
        to { opacity: 1; transform: translateY(0); } /* 최종 상태: 완전 불투명, 원래 위치 */
      }
      
      /* 박스 상단과 왼쪽 선 애니메이션 */
      @keyframes drawBoxPart1 {
        0% { stroke-dasharray: 0 40; }
        100% { stroke-dasharray: 40 0; }
      }
      
      /* 박스 하단과 오른쪽 선 애니메이션 */
      @keyframes drawBoxPart2 {
        0% { stroke-dasharray: 0 40; }
        100% { stroke-dasharray: 40 0; }
      }
      
      /* 체크 표시 그리기 애니메이션 */
      @keyframes drawCheck {
        0% { stroke-dasharray: 0 30; }
        100% { stroke-dasharray: 30 0; }
      }

      /* fade in 효과 */
      @keyframes fadeIn {
        from { opacity: 0; } /* 처음에는 투명 */
        to { opacity: 1; } /* 완전히 나타남 */
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
      
      /* 일반 텍스트 스타일 */
      text {
        font-family: "Open Sans", sans-serif;
        fill: white;
        font-size: 22px;
        opacity: 0;
        animation: fadeIn 1s ease-in-out forwards;
        dominant-baseline: middle;
      }
      
      /* 이름 텍스트 스타일 */
      text.name {
        font-size: 30px;
        font-weight: bold;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 0.6s;
      }

      /* 직업 텍스트 스타일 */
      text.job {
        font-size: 18px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1s;
      }

      /* 회사 텍스트 스타일 */
      text.company {
        font-size: 18px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.2s;
      }

      /* 주소 텍스트 스타일 */
      text.address {
        fill: #777777;
        font-size: 15px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.4s;
      }

      /* 한줄소개 */
      text.about {
        fill: white;
        font-size: 22px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.8s;
      }

      /* 한줄소개 본문 */
      text.about-content {
        fill: #979696;
        font-size: 15px;
        font-weight: 1;
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.9s;
      }
          
      /* 주소 아이콘 */
      .address-icon { 
        fill: #777777;
        opacity: 0; /* 초기 상태에서 숨김 */
        animation: fadeIn 0.5s ease-in-out forwards; animation-delay: 1.5s;
      }

      /* 아이콘(박스) 애니메이션 */
      .icon line {
        stroke: white;
        stroke-width: 1.5;
        fill: none;
      }
      
      /* 상단과 왼쪽 선 애니메이션 */
      .icon .top-left {
        stroke-dasharray: 40;
        stroke-dashoffset: 40;
        animation-delay: 3s;
        animation: drawBoxPart1 1s forwards; animation-delay: 2.6s;
      }
      
      /* 하단과 오른쪽 선 애니메이션 */
      .icon .bottom-right {
        stroke-dasharray: 40;
        stroke-dashoffset: 40;
        animation: drawBoxPart2 1s forwards; animation-delay: 2.8s;
      }
      
      /* 체크 표시 애니메이션 */
      .check {
        stroke: white;
        stroke-width: 1.5;
        fill: none;
        stroke-dasharray: 30;
        stroke-dashoffset: 30;
        animation: drawCheck 0.5s forwards; animation-delay: 3s;
      }

      .icon:hover line, .icon:hover .check {
        stroke: #3498db; /* 원하는 파랑색 코드로 변경 가능 */
        transition: stroke 0.3s ease; /* 부드러운 색 전환을 위한 트랜지션 */
        cursor: pointer; /* 커서를 포인터로 변경 */
      }

      .linkedin {
        opacity: 0; /* 초기 상태에서 숨김 */
        animation: fadeIn 1.5s ease-in-out forwards; animation-delay: 2s;
      }

    </style>
  </defs>
  
  <!-- 배경 사각형: 선형 그라디언트를 적용한 배경 -->
  <rect x="10" y="10" width="400" height="230" rx="0" ry="0" fill="url(#grad)" />

  <!-- 별 효과 -->
  <g id="stars">
    <circle class="twinkling-star" cx="50" cy="30" r="1.1" style="animation-delay: 0s;"/>
    <circle class="twinkling-star" cx="300" cy="50" r="1.3" style="animation-delay: 1s;"/>
    <circle class="twinkling-star" cx="290" cy="30" r="1" style="animation-delay: 2s;"/>
    <circle class="twinkling-star" cx="240" cy="100" r="1.4" style="animation-delay: 3s;"/>
    <circle class="twinkling-star" cx="370" cy="140" r="1.5" style="animation-delay: 4s;"/>
  </g>

  <!-- 이름 -->
  <text class="name" x="50" y="60">Abraham Wakarella</text>

  <!-- 직업 -->
  <text class="job" x="50" y="90">Developer - Assistant</text>
  <!-- 회사(소속) -->
  <text class="company" x="50" y="115">Mobidick Co., Ltd</text>
  <!-- 주소 아이콘 + 텍스트 -->
  <g transform="translate(45, 135)">
    <text class="address" x="30" y="13">Doksan, Seoul, Republic of Korea.</text>
    <path class="address-icon" d="M12 2C8.686 2 6 4.686 6 8C6 12.627 12 21 12 21C12 21 18 12.627 18 8C18 4.686 15.314 2 12 2zM12 10C10.895 10 10 9.105 10 8C10 6.895 10.895 6 12 6C13.105 6 14 6.895 14 8C14 9.105 13.105 10 12 10z" />
  </g>

  <!-- 한줄소개 -->
  <text class="about" x="50" y="190">About Me</text>
  <text class="about-content" x="50" y="210">Merry go round of life.</text>


  <!-- 이메일 아이콘 링크: 클릭하면 이메일을 보낼 수 있음 -->
  <a href="mailto:example@email.com">
    <g class="icon" transform="translate(377, 20) rotate(45)"> <!-- 아이콘 위치 및 회전 적용 -->
       <!-- 투명 사각형: 호버 영역 확대 -->
      <rect x="-5" y="-5" width="30" height="30" fill="transparent" pointer-events="all" />

      <!-- 상단 선 -->
      <line class="top-left" x1="-0.5" y1="0.5" x2="20.5" y2="0.5" />
      <!-- 왼쪽 선 -->
      <line class="top-left" x1="0" y1="0" x2="0" y2="15" />
      <!-- 하단 선 -->
      <line class="bottom-right" x1="-0.5" y1="14.5" x2="20.5" y2="14.5" />
      <!-- 오른쪽 선 -->
      <line class="bottom-right" x1="20" y1="0" x2="20" y2="15" />
      
      <!-- 체크 표시 -->
      <polyline class="check" points="0.5,0.5 10,10 19.5,1" /> <!-- 체크 아이콘 -->
    </g>
  </a>

  <!-- 링크드인 아이콘 -->
  <a href="https://www.linkedin.com/feed/">
    <g class="linkedin" transform="translate(340, 180) scale(1)">
      <path fill="#c37d16" d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5V37z"></path>
      <path fill="#FFF" d="M12 19H17V36H12zM14.485 17h-.028C12.965 17 12 15.888 12 14.499 12 13.08 12.995 12 14.514 12c1.521 0 2.458 1.08 2.486 2.499C17 15.887 16.035 17 14.485 17zM36 36h-5v-9.099c0-2.198-1.225-3.698-3.192-3.698-1.501 0-2.313 1.012-2.707 1.99C24.957 25.543 25 26.511 25 27v9h-5V19h5v2.616C25.721 20.5 26.85 19 29.738 19c3.578 0 6.261 2.25 6.261 7.274L36 36 36 36z"></path>
    </g>
  </a>
</svg>'''
  return svg
