import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np

# Set professional styling
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# Create figure with high DPI for crisp output
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')
fig.patch.set_facecolor('white')

# NASA-style professional colors
colors = {
    'executive': '#0B3D91',    # NASA Blue
    'management': '#1F4E79',   # Dark Blue
    'engineering': '#228B22',  # Forest Green
    'science': '#CD853F',      # Peru/Bronze
    'support': '#4B0082'       # Indigo
}

# Helper function to create professional rectangular boxes
def create_box(ax, x, y, width, height, text, color, text_size=10, text_color='white', border_color='#333333'):
    # Create main box
    box = Rectangle((x-width/2, y-height/2), width, height,
                   facecolor=color, 
                   edgecolor=border_color,
                   linewidth=1.5,
                   alpha=0.9)
    ax.add_patch(box)
    
    # Add subtle shadow effect
    shadow = Rectangle((x-width/2+0.05, y-height/2-0.05), width, height,
                      facecolor='gray', 
                      alpha=0.3,
                      zorder=0)
    ax.add_patch(shadow)
    
    # Handle text formatting
    lines = text.split('\n')
    if len(lines) <= 2:
        ax.text(x, y, text, ha='center', va='center', 
                fontsize=text_size, fontweight='bold', color=text_color,
                family='Arial')
    else:
        # For multi-line text, adjust spacing
        total_height = len(lines) * 0.15
        start_y = y + total_height/2
        
        for i, line in enumerate(lines):
            line_y = start_y - (i * 0.15)
            # Make first line bold and slightly larger
            if i == 0:
                ax.text(x, line_y, line, ha='center', va='center', 
                       fontsize=text_size, fontweight='bold', color=text_color,
                       family='Arial')
            else:
                ax.text(x, line_y, line, ha='center', va='center', 
                       fontsize=text_size-1, fontweight='normal', color=text_color,
                       family='Arial')

# Helper function to draw professional connecting lines
def draw_line(ax, x1, y1, x2, y2, linewidth=1.5, color='#333333'):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, solid_capstyle='round')

# Helper function to draw organizational tree lines
def draw_org_lines(ax, parent_x, parent_y, children_positions, drop_distance=0.5):
    if len(children_positions) == 1:
        child_x, child_y = children_positions[0]
        # Direct line for single child
        draw_line(ax, parent_x, parent_y - 0.4, parent_x, parent_y - drop_distance)
        draw_line(ax, parent_x, parent_y - drop_distance, child_x, parent_y - drop_distance)
        draw_line(ax, child_x, parent_y - drop_distance, child_x, child_y + 0.4)
    else:
        # Multi-child tree structure
        min_x = min([pos[0] for pos in children_positions])
        max_x = max([pos[0] for pos in children_positions])
        
        # Vertical line down from parent
        draw_line(ax, parent_x, parent_y - 0.4, parent_x, parent_y - drop_distance)
        # Horizontal line across children
        draw_line(ax, min_x, parent_y - drop_distance, max_x, parent_y - drop_distance)
        
        # Lines down to each child
        for child_x, child_y in children_positions:
            draw_line(ax, child_x, parent_y - drop_distance, child_x, child_y + 0.4)

# Header with NASA styling
ax.text(10, 13.2, 'MARS ROVER MISSION', ha='center', va='center', 
        fontsize=20, fontweight='bold', color='#0B3D91', family='Arial')
ax.text(10, 12.8, 'ORGANIZATIONAL STRUCTURE', ha='center', va='center', 
        fontsize=16, fontweight='bold', color='#333333', family='Arial')

# Add NASA logo placeholder or mission identifier
ax.text(1, 12.8, 'L\'SPACE ACADEMY', ha='left', va='center', 
        fontsize=12, fontweight='bold', color='#0B3D91', family='Arial')
ax.text(19, 12.8, 'PHASES C-F', ha='right', va='center', 
        fontsize=12, fontweight='bold', color='#0B3D91', family='Arial')

# Level 1: Project Manager
create_box(ax, 10, 11.2, 4, 0.8, 'PROJECT MANAGER', colors['executive'], 12)

# Level 2: Deputy PM
create_box(ax, 10, 10.1, 4.5, 0.7, 'DEPUTY PM OF RESOURCES', colors['executive'], 11)
draw_line(ax, 10, 10.8, 10, 10.45)

# Level 3: Key Management (properly spaced)
management_y = 8.8
management_positions = [
    ('SYSTEMS ENGINEERING\n& INTEGRATION', 3.5, management_y),
    ('PROGRAM MANAGEMENT\n& FINANCE', 10, management_y),
    ('MISSION ASSURANCE', 16.5, management_y)
]

# Draw lines to management level
draw_org_lines(ax, 10, 9.75, [(pos[1], pos[2]) for pos in management_positions], 0.5)

for title, x, y in management_positions:
    create_box(ax, x, y, 3.2, 0.8, title, colors['management'], 10)

# Level 4: Division Headers (properly aligned)
division_y = 7.3
divisions = [
    ('ENGINEERING', 3.5, division_y, colors['engineering']),
    ('SCIENCE & OPERATIONS', 10, division_y, colors['science']),
    ('SUPPORT SERVICES', 16.5, division_y, colors['support'])
]

# Connect divisions to management
for i, (title, x, y, color) in enumerate(divisions):
    create_box(ax, x, y, 4, 0.6, title, color, 11)
    # Connect to corresponding management position
    draw_line(ax, management_positions[i][1], management_y - 0.4, x, y + 0.3)

# Level 5: Engineering Subteams (evenly spaced)
eng_y = 5.8
eng_teams = [
    ('MECHANICAL\nINTEGRATION', 1, eng_y),
    ('POWER & ELECTRICAL\nSYSTEMS', 2.5, eng_y),
    ('THERMAL &\nENVIRONMENTAL', 4, eng_y),
    ('SOFTWARE &\nCOMPUTER SYSTEMS', 5.5, eng_y)
]

draw_org_lines(ax, 3.5, division_y - 0.3, [(team[1], team[2]) for team in eng_teams], 0.8)

for title, x, y in eng_teams:
    create_box(ax, x, y, 2.2, 1, title, colors['engineering'], 9)
    # Add staffing info below
    ax.text(x, y - 0.7, '4-6 → 2-3', ha='center', va='center', 
            fontsize=8, style='italic', color='#666666', family='Arial')

# Level 5: Science & Operations Subteams
sci_y = 5.8
sci_teams = [
    ('PAYLOAD\nSCIENCE', 8.5, sci_y),
    ('MISSION\nOPERATIONS', 10, sci_y),
    ('VALIDATION &\nVERIFICATION', 11.5, sci_y)
]

draw_org_lines(ax, 10, division_y - 0.3, [(team[1], team[2]) for team in sci_teams], 0.8)

for title, x, y in sci_teams:
    create_box(ax, x, y, 2.2, 1, title, colors['science'], 9, 'white')
    # Add staffing info below
    if 'PAYLOAD' in title:
        ax.text(x, y - 0.7, '3-4 → 6-8', ha='center', va='center', 
                fontsize=8, style='italic', color='#666666', family='Arial')
    elif 'OPERATIONS' in title:
        ax.text(x, y - 0.7, '2-3 → 4-6', ha='center', va='center', 
                fontsize=8, style='italic', color='#666666', family='Arial')
    else:
        ax.text(x, y - 0.7, '3-4 → 2-3', ha='center', va='center', 
                fontsize=8, style='italic', color='#666666', family='Arial')

# Level 5: Support Subteams
support_y = 5.8
support_teams = [
    ('COMMUNICATIONS\n& OUTREACH', 15, support_y),
    ('ADMINISTRATION\n& PROCUREMENT', 16.5, support_y),
    ('TECHNICIANS &\nTEST SUPPORT', 18, support_y)
]

draw_org_lines(ax, 16.5, division_y - 0.3, [(team[1], team[2]) for team in support_teams], 0.8)

for title, x, y in support_teams:
    create_box(ax, x, y, 2.2, 1, title, colors['support'], 9)
    # Add staffing info below
    if 'TECHNICIANS' in title:
        ax.text(x, y - 0.7, 'Variable', ha='center', va='center', 
                fontsize=8, style='italic', color='#666666', family='Arial')
    else:
        ax.text(x, y - 0.7, '1-2 → 1-2', ha='center', va='center', 
                fontsize=8, style='italic', color='#666666', family='Arial')

# Level 6: Specialized Teams under Payload Science
special_y = 4.2
special_teams = [
    ('ASTROBIOLOGY', 7.5, special_y),
    ('GEOLOGY', 8.5, special_y),
    ('PAYLOAD SPECIALISTS', 9.5, special_y)
]

draw_org_lines(ax, 8.5, sci_y - 0.5, [(team[1], team[2]) for team in special_teams], 0.4)

for title, x, y in special_teams:
    create_box(ax, x, y, 1.8, 0.6, title, colors['science'], 8, 'white')

# Professional information boxes
# Mission Phases Box
phase_box = Rectangle((0.2, 1.8), 6, 2.8, facecolor='#f8f9fa', 
                     edgecolor='#dee2e6', linewidth=1.5, alpha=0.95)
ax.add_patch(phase_box)
ax.text(0.4, 4.4, 'MISSION PHASES', ha='left', va='top', 
        fontsize=12, fontweight='bold', color='#0B3D91', family='Arial')

phase_text = """PHASES C & D (Design & Fabrication):
• Engineering-focused team structure
• Hardware integration & testing
• System verification & validation
• Payload calibration & interfaces

PHASES E & F (Operations & Science):
• Science-focused team expansion
• Mission operations & monitoring
• Data collection & analysis
• Scientific interpretation & reporting"""

ax.text(0.4, 4.1, phase_text, ha='left', va='top', fontsize=9, 
        color='#333333', family='Arial')

# Coordination Structure Box
coord_box = Rectangle((13.8, 1.8), 6, 2.8, facecolor='#f8f9fa', 
                     edgecolor='#dee2e6', linewidth=1.5, alpha=0.95)
ax.add_patch(coord_box)
ax.text(14, 4.4, 'COORDINATION STRUCTURE', ha='left', va='top', 
        fontsize=12, fontweight='bold', color='#0B3D91', family='Arial')

coord_text = """SYSTEMS ENGINEERING & INTEGRATION:
• Cross-functional interface management
• Configuration control & ICDs
• Integrated testing coordination

SUBTEAM AUTONOMY:
• Design-level decision authority
• Discretionary resource allocation
• Direct progress reporting

CENTRALIZED OVERSIGHT:
• Strategic resource management
• Risk assessment & mitigation
• Quality assurance & compliance"""

ax.text(14, 4.1, coord_text, ha='left', va='top', fontsize=9, 
        color='#333333', family='Arial')

# Professional legend
legend_y = 1.2
legend_elements = [
    patches.Rectangle((0, 0), 1, 1, facecolor=colors['executive'], label='Executive Leadership'),
    patches.Rectangle((0, 0), 1, 1, facecolor=colors['management'], label='Management'),
    patches.Rectangle((0, 0), 1, 1, facecolor=colors['engineering'], label='Engineering'),
    patches.Rectangle((0, 0), 1, 1, facecolor=colors['science'], label='Science & Operations'),
    patches.Rectangle((0, 0), 1, 1, facecolor=colors['support'], label='Support Services')
]

legend = ax.legend(handles=legend_elements, loc='center', bbox_to_anchor=(10, legend_y), 
                 ncol=5, fontsize=10, frameon=True, fancybox=True, shadow=True)
legend.get_frame().set_facecolor('#f8f9fa')
legend.get_frame().set_edgecolor('#dee2e6')

# Footer information
ax.text(10, 0.6, 'Personnel allocation shown as: Phase C-D → Phase E-F', 
        ha='center', va='center', fontsize=10, style='italic', 
        color='#666666', family='Arial')
ax.text(10, 0.2, 'Total Mission Team: 25-30 personnel (excluding Academy core team)', 
        ha='center', va='center', fontsize=10, fontweight='bold', 
        color='#0B3D91', family='Arial')

plt.savefig('/Users/azrabano/ru_law-analysis-tool/mission_org_chart_nasa.png', 
            dpi=400, bbox_inches='tight', facecolor='white', pad_inches=0.3)
plt.close()

print("NASA-quality organizational chart saved as 'mission_org_chart_nasa.png')")
print("Opening the chart...")

# Open the image
import subprocess
subprocess.run(['open', '/Users/azrabano/ru_law-analysis-tool/mission_org_chart_nasa.png'])
