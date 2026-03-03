<style>
  .hobby-container {
    display: flex;
    gap: 16px;
    margin-top: 35px;
    margin-bottom: 30px;
    align-items: center;
    font-size: 0.95em;
  }
  
  .tooltip-item {
    position: relative;
    display: flex;
    align-items: center;
    cursor: default;
  }
  
  .hobby-emoji {
    font-size: 1.3em;
    transition: transform 0.2s ease, filter 0.2s ease;
    filter: grayscale(0.2);
    user-select: none;
  }
  
  .tooltip-item:hover .hobby-emoji {
    transform: scale(1.15);
    filter: grayscale(0);
  }

  /* Tooltip logic */
  .tooltip-item .tooltip-text {
    visibility: hidden;
    background-color: #232F3E;
    color: #fff;
    text-align: center;
    padding: 6px 10px;
    border-radius: 6px;
    position: absolute;
    z-index: 10;
    bottom: 130%;
    left: 50%;
    transform: translateX(-50%) translateY(5px);
    opacity: 0;
    transition: opacity 0.2s ease, transform 0.2s ease;
    font-size: 0.8em;
    font-weight: 500;
    white-space: nowrap;
    pointer-events: none;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }

  .tooltip-item .tooltip-text::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #232F3E transparent transparent transparent;
  }

  .tooltip-item:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  
  .hobby-divider {
    color: #ccc;
    font-size: 1.2em;
    margin: 0;
    user-select: none;
    pointer-events: none;
  }

  /* Writing links logic */
  .writing-item {
    display: flex;
    align-items: center;
    cursor: default;
  }
  
  .writing-item .hobby-emoji {
    cursor: pointer;
  }

  .writing-item:hover .hobby-emoji {
    transform: scale(1.15);
    filter: grayscale(0);
  }

  .writing-links {
    max-width: 0;
    overflow: hidden;
    white-space: nowrap;
    opacity: 0;
    transition: max-width 0.5s ease 0.1s, opacity 0.4s ease 0.1s, margin-left 0.4s ease 0.1s;
    display: flex;
    gap: 16px;
    align-items: center;
  }

  .writing-item:hover .writing-links {
    max-width: 600px;
    opacity: 1;
    margin-left: 14px;
  }

  .writing-link {
    color: #666;
    text-decoration: none;
    font-size: 0.9em;
    font-weight: 500;
    transition: color 0.2s ease;
  }

  .writing-link:hover {
    color: #FF7900;
  }

  .external-icon {
    font-size: 0.7em;
    margin-left: 3px;
    opacity: 0.5;
    vertical-align: super;
  }
</style>

<div class="hobby-container">
  <span style="color: #999; font-size: 0.85em; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-right: -4px;">Hobbies:</span>
  
  <!-- Tooltip Items -->
  <div class="tooltip-item">
    <span class="hobby-emoji">😋</span>
    <span class="tooltip-text">Trying new restaurants</span>
  </div>
  
  <div class="tooltip-item">
    <span class="hobby-emoji">👩‍💻</span>
    <span class="tooltip-text">Browsing for tools</span>
  </div>
  
  <div class="tooltip-item">
    <span class="hobby-emoji">🏀</span>
    <span class="tooltip-text">Basketball, Running</span>
  </div>

  <span class="hobby-divider">|</span>

  <!-- Expanding Links Item -->
  <div class="writing-item">
    <a href="#blog" style="text-decoration: none; display: flex; align-items: center;">
      <span style="color: #999; font-size: 0.85em; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 8px; transition: color 0.2s;" onmouseover="this.style.color='#FF7900'" onmouseout="this.style.color='#999'">Blog:</span>
      <span class="hobby-emoji" title="Read my blogs">✍️</span>
    </a>
  </div>
</div>
