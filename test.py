import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rc_circuit():
    fig, ax = plt.subplots(figsize=(6,4))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # Draw input voltage source
    ax.plot([-1.5, -1], [1, 1], 'black', linewidth=2)  # Wire to voltage source
    ax.add_patch(patches.Rectangle((-1.6, 0.9), 0.2, 0.2, color='black'))  # Voltage source
    ax.text(-1.8, 1, "V_in", fontsize=12, color='black', verticalalignment='center')
    
    # Draw resistor
    ax.plot([-1, 0], [1, 1], 'black', linewidth=2)  # Wire to resistor
    ax.add_patch(patches.Rectangle((-0.3, 0.9), 0.6, 0.2, fill=False, edgecolor='black', linewidth=2))  # Resistor
    ax.text(0, 1.2, "R", fontsize=12, color='black', verticalalignment='center')
    
    # Draw capacitor
    ax.plot([0, 0], [1, 0], 'black', linewidth=2)  # Wire to capacitor
    ax.plot([-0.3, -0.3], [0, -0.3], 'black', linewidth=2)  # Capacitor plate 1
    ax.plot([0.3, 0.3], [0, -0.3], 'black', linewidth=2)  # Capacitor plate 2
    ax.text(0.1, -0.1, "C", fontsize=12, color='black', verticalalignment='center')
    
    # Close the circuit
    ax.plot([-1.5, -1.5], [0, 1], 'black', linewidth=2)  # Wire back to voltage source
    ax.plot([-1.5, 0], [0, 0], 'black', linewidth=2)  # Bottom wire
    
    plt.show()

draw_rc_circuit()
