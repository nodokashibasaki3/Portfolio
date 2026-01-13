<div class="exp-toggle-wrapper" style="margin-top: 20px; margin-bottom: 10px;">
    <span id="exp-toggle" class="exp-toggle-btn profile-text" style="cursor: pointer; color: #333; font-weight: normal;">▶︎ toggle here for experience timeline!</span>
</div>

<div id="exp-experience-outer" class="experience">
    <div class="table-responsive">
        <table class="table table-sm table-borderless" style="border-collapse: collapse;">
            {% for item in site.data.experience %}
            <tr style="border: none;">
                <th scope="row" style="width: 15%; min-width: 100px; border: none; padding: 2px 10px; {% if item.highlight %}color: #d32f2f;{% endif %}">{{ item.duration }}</th>
                <td style="border: none; padding: 2px 10px; {% if item.highlight %}background-color: rgba(211, 47, 47, 0.05);{% endif %}">
                    {{ item.position }}
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>

<script>
// Experience toggle show/hide with animation
document.addEventListener('DOMContentLoaded', function() {
    const expToggle = document.getElementById('exp-toggle');
    const expOuter = document.getElementById('exp-experience-outer');
    let expOpen = false; // Default to closed
    
    if (expToggle && expOuter) {
        expToggle.addEventListener('click', function() {
            expOpen = !expOpen;
            if (expOpen) {
                expOuter.style.maxHeight = expOuter.scrollHeight + 'px';
                expOuter.style.opacity = '1';
                expToggle.textContent = '▼ in-depth experience timeline...';
            } else {
                expOuter.style.maxHeight = '0px';
                expOuter.style.opacity = '0';
                expToggle.textContent = '▶︎ in-depth experience timeline...';
            }
        });
        // Set initial state
        expOuter.style.overflow = 'hidden';
        expOuter.style.transition = 'max-height 0.5s cubic-bezier(0.4,0,0.2,1), opacity 0.4s';
        expOuter.style.maxHeight = '0px';
        expOuter.style.opacity = '0';
    }
});
</script>
