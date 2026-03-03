<div class="technical-journey" style="margin: 40px 0;">
    <h3 style="font-size: 1.1em; font-weight: 600; color: #222; margin-bottom: 25px; letter-spacing: 0.02em;">Timeline</h3>
    
    <div style="position: relative;">
        <!-- Vertical Line -->
        <div style="position: absolute; left: 79.49999618px; top: 12px; bottom: 12px; width: 1px; background-color: #eee; z-index: 0;"></div>

        {% assign exp_size = site.data.experience | size %}
        {% assign hide_limit = exp_size | minus: 5 %}
        {% for item in site.data.experience %}
        <div class="experience-item {% if forloop.index <= hide_limit %}hidden-exp{% endif %}" style="display: {% if forloop.index <= hide_limit %}none{% else %}flex{% endif %}; margin-bottom: 5px; position: relative; align-items: flex-start;">
            <!-- Duration -->
            <div style="width: 65px; text-align: right; margin-right: 30px; font-size: 0.85em; color: #999; padding-top: 5px; flex-shrink: 0;">
                {{ item.duration }}
            </div>

            <!-- Dot Container -->
            <div style="position: absolute; left: 80px; top: 13px; transform: translate(-50%, -50%); z-index: 2;">
                <div style="width: 8px; height: 8px; background-color: {% if item.highlight %}#FF7900{% else %}#ddd{% endif %}; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 0 0 1px #fff;"></div>
            </div>

            <!-- Content -->
            <div style="flex-grow: 1; padding-left: 10px;">
                <div style="font-size: 0.95em; color: #333; line-height: 1.4; {% if item.highlight %}background-color: rgba(255, 121, 0, 0.05); padding: 4px 10px; border-radius: 4px; margin-left: -10px; font-weight: 500;{% endif %}">
                    {{ item.position }}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    <div style="text-align: center; margin-top: 20px;">
        <button id="toggle-experience-btn" onclick="toggleExperience()" style="background: none; border: none; padding: 0; outline: none; color: #999; font-family: inherit; font-size: 0.8075em; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; transition: color 0.2s ease;" onmouseover="this.style.color='#FF7900'" onmouseout="this.style.color='#999'">SHOW FULL TIMELINE ▼</button>
    </div>
</div>

<script>
function toggleExperience() {
    var items = document.querySelectorAll('.experience-item.hidden-exp');
    var btn = document.getElementById('toggle-experience-btn');
    if (!items || items.length === 0) return;
    
    var isHidden = items[0].style.display === 'none';
    
    for (var i = 0; i < items.length; i++) {
        items[i].style.display = isHidden ? 'flex' : 'none';
    }
    
    btn.innerHTML = isHidden ? 'SHOW LESS ▲' : 'SHOW FULL TIMELINE ▼';
}
</script>
