import matplotlib.pyplot as plt

def plot_figures(X,Y,xlabels=None,ylabels=None,titles=None,ncol=1,cell_width=1,cell_height=1,
                 left_margin=0.5,right_margin=0.5,top_margin=0.5,bottom_margin=0.5,
                 h_margin=0.5,v_margin=0.5,fmts=None,grid=None,solid_markers=None, 
                 legends=None,dstfile=None,xlims=None,ylims=None):
    """
    Function to plot multiple subplots, with individual settings for grid and solid/hollow markers.

    Parameters:
    X: list, x-axis data for each subplot, each entry can be a list of lists for multiple curves in one subplot
    Y: list, y-axis data for each subplot, each entry can be a list of lists for multiple curves in one subplot
    xlabels: list, x-axis labels for each subplot
    ylabels: list, y-axis labels for each subplot
    titles: list, titles for each subplot
    ncol: int, number of subplots per row
    cell_width: float, width of each subplot
    cell_height: float, height of each subplot
    left_margin: float, left margin for the entire figure
    right_margin: float, right margin for the entire figure
    top_margin: float, top margin for the entire figure
    bottom_margin: float, bottom margin for the entire figure
    h_margin: float, horizontal margin between subplots
    v_margin: float, vertical margin between subplots
    fmts: list of lists, format for line style, markers, colors for each subplot and each curve
    grid: list, whether to display grid, set individually for each subplot
    solid_markers: list of lists, whether markers should be solid or hollow, set individually for each subplot and each curve
    dstfile: str, filename to save the figure, None means do not save
    xlims: list of tuples, x-axis limits for each subplot, e.g., [(xmin1, xmax1), (xmin2, xmax2), ...]
    ylims: list of tuples, y-axis limits for each subplot, e.g., [(ymin1, ymax1), (ymin2, ymax2), ...]
    """

    n_plots = len(X)
    
    # If only one set of data, force ncol = 1, h_margin = 0, v_margin = 0
    if n_plots == 1:
        ncol = 1
        h_margin = 0
        v_margin = 0
    
    nrow = (n_plots + ncol - 1) // ncol  # Calculate the number of rows needed
    
    # Total figure width and height
    fig_width = ncol * cell_width + left_margin + right_margin + (ncol - 1) * h_margin
    fig_height = nrow * cell_height + top_margin + bottom_margin + (nrow - 1) * v_margin
    
    fig, axes = plt.subplots(nrow, ncol, figsize=(fig_width, fig_height))
    
    # Check if axes is a single object or an array
    if n_plots == 1:
        axes = [axes]  # Convert to a list to maintain consistency in handling
    else:
        axes = axes.flatten()  # Flatten the axes array if there are multiple subplots
    
    for i in range(n_plots):
        # If X[i] is a list of multiple curves, we iterate over them
        if isinstance(X[i][0], list):  # Detect multiple curves in one subplot
            for j, (x_data, y_data) in enumerate(zip(X[i], Y[i])):
                fmt = fmts[i][j] if fmts and len(fmts) > i and len(fmts[i]) > j else '-'  # Line style format
                
                # Control marker fill color
                if solid_markers and len(solid_markers) > i and len(solid_markers[i]) > j:
                    markerfacecolor = 'none' if not solid_markers[i][j] else None
                else:
                    markerfacecolor = None        
                
                # Set the label for the legend if provided
                legend_label = legends[i][j] if legends and len(legends) > i and legends[i] is not None and len(legends[i]) > j else None
                
                # Plot the data
                line, = axes[i].plot(x_data, y_data, fmt, markerfacecolor=markerfacecolor, label=legend_label)
        else:
            # Single curve case
            fmt = fmts[i][0] if fmts and len(fmts) > i and len(fmts[i]) > 0 else '-'
            markerfacecolor = 'none' if solid_markers and len(solid_markers) > i and not solid_markers[i] else None
                   
            # Set the label for the legend if provided
            legend_label = legends[i] if legends and len(legends) > i and legends[i] is not None else None
            
            # Plot the data
            line, = axes[i].plot(X[i], Y[i], fmt, markerfacecolor=markerfacecolor, label=legend_label)
    
        # Set xlim and ylim if provided
        if xlims and len(xlims) > i:
            axes[i].set_xlim(xlims[i])
        if ylims and len(ylims) > i:
            axes[i].set_ylim(ylims[i])
            
        # Control grid display
        if grid and len(grid) > i:
            axes[i].grid(grid[i])
        
        if xlabels:
            axes[i].set_xlabel(xlabels[i])
        if ylabels:
            axes[i].set_ylabel(ylabels[i])
        if titles:
            axes[i].set_title(titles[i])
        
        # Show legend if it exists
        if legends and len(legends) > i and legends[i] is not None:
            axes[i].legend()

    # Hide any extra subplots
    for j in range(n_plots, len(axes)):
        axes[j].axis('off')
    
    plt.subplots_adjust(left=left_margin/fig_width, right=1-right_margin/fig_width, 
                        top=1-top_margin/fig_height, bottom=bottom_margin/fig_height,
                        wspace=h_margin/cell_width, hspace=v_margin/cell_height)
    
    if dstfile:
        plt.savefig(dstfile)
    
    plt.show()

def plot_2d_maps(X, titles=None, ncol=1, cell_width=None, cell_height=1,
                 left_margin=0.5, right_margin=0.5, top_margin=0.5, bottom_margin=0.5,
                 h_margin=0.5, v_margin=0.5, colorbars=None, cmaps=None,
                 dstfile=None, show_axes=True):
    """
    Function to display multiple 2D data as subplots.

    Parameters:
    X: list of 2D arrays, the data to display
    titles: list of str, titles for each subplot
    ncol: int, number of columns in the subplot grid
    cell_width: float, width of each subplot
    cell_height: float, height of each subplot (default is 1)
    left_margin, right_margin, top_margin, bottom_margin: float, margins around the figure
    h_margin: float, horizontal margin between subplots
    v_margin: float, vertical margin between subplots
    colorbars: list of bool, whether to display a colorbar for each subplot
    cmaps: list of str, colormaps to use for each subplot
    dstfile: str, filename to save the figure, None means do not save
    show_axes: bool, whether to display axes on the subplots
    """
    n_plots = len(X)
    
    # Set default cell_width based on the size of the first dataset
    if cell_width is None:
        first_data_shape = X[0].shape
        aspect_ratio = first_data_shape[1] / first_data_shape[0]  # Width / Height
        cell_width = cell_height * aspect_ratio  # Set cell_width based on the aspect ratio

    nrow = (n_plots + ncol - 1) // ncol  # Calculate the number of rows needed

    # Total figure width and height
    fig_width = ncol * cell_width + left_margin + right_margin + (ncol - 1) * h_margin
    fig_height = nrow * cell_height + top_margin + bottom_margin + (nrow - 1) * v_margin
    
    fig, axes = plt.subplots(nrow, ncol, figsize=(fig_width, fig_height))

    # Check if axes is a single object or an array
    if n_plots == 1:
        axes = [axes]  # Convert to a list to maintain consistency in handling
    else:
        axes = axes.flatten()  # Flatten the axes array if there are multiple subplots

    for i in range(n_plots):
        # Set the colormap
        cmap = cmaps[i] if cmaps and len(cmaps) > i else 'viridis'
        
        # Display the data as an image
        im = axes[i].imshow(X[i], cmap=cmap, aspect='auto')

        # Add colorbar if specified
        if colorbars and len(colorbars) > i and colorbars[i]:
            plt.colorbar(im, ax=axes[i])
        
        # Set title for each subplot
        if titles and len(titles) > i:
            axes[i].set_title(titles[i])

        # Show or hide axes
        if not show_axes:
            axes[i].axis('off')

    # Hide any extra subplots
    for j in range(n_plots, len(axes)):
        axes[j].axis('off')

    # Adjust layout
    plt.subplots_adjust(left=left_margin/fig_width, right=1-right_margin/fig_width, 
                        top=1-top_margin/fig_height, bottom=bottom_margin/fig_height,
                        wspace=h_margin/cell_width, hspace=v_margin/cell_height)

    if dstfile:
        plt.savefig(dstfile)
    
    plt.show()

def plot_imgs(X, titles=None, ncol=1, cell_width=None, cell_height=1,
                 left_margin=0.5, right_margin=0.5, top_margin=0.5, bottom_margin=0.5,
                 h_margin=0.5, v_margin=0.5, 
                 dstfile=None, show_axes=False):
    """
    Function to display multiple image as subplots.

    Parameters:
    X: list of rgb images, the data to display
    titles: list of str, titles for each subplot
    ncol: int, number of columns in the subplot grid
    cell_width: float, width of each subplot
    cell_height: float, height of each subplot (default is 1)
    left_margin, right_margin, top_margin, bottom_margin: float, margins around the figure
    h_margin: float, horizontal margin between subplots
    v_margin: float, vertical margin between subplots
    dstfile: str, filename to save the figure, None means do not save
    show_axes: bool, whether to display axes on the subplots
    """
    n_plots = len(X)
    
    # Set default cell_width based on the size of the first dataset
    if cell_width is None:
        first_data_shape = X[0].shape
        aspect_ratio = first_data_shape[1] / first_data_shape[0]  # Width / Height
        cell_width = cell_height * aspect_ratio  # Set cell_width based on the aspect ratio

    nrow = (n_plots + ncol - 1) // ncol  # Calculate the number of rows needed

    # Total figure width and height
    fig_width = ncol * cell_width + left_margin + right_margin + (ncol - 1) * h_margin
    fig_height = nrow * cell_height + top_margin + bottom_margin + (nrow - 1) * v_margin
    
    fig, axes = plt.subplots(nrow, ncol, figsize=(fig_width, fig_height))

    # Check if axes is a single object or an array
    if n_plots == 1:
        axes = [axes]  # Convert to a list to maintain consistency in handling
    else:
        axes = axes.flatten()  # Flatten the axes array if there are multiple subplots

    for i in range(n_plots):  
        # Display the data as an image
        im = axes[i].imshow(X[i])

        # Set title for each subplot
        if titles and len(titles) > i:
            axes[i].set_title(titles[i])

        # Show or hide axes
        if not show_axes:
            axes[i].axis('off')

    # Hide any extra subplots
    for j in range(n_plots, len(axes)):
        axes[j].axis('off')

    # Adjust layout
    plt.subplots_adjust(left=left_margin/fig_width, right=1-right_margin/fig_width, 
                        top=1-top_margin/fig_height, bottom=bottom_margin/fig_height,
                        wspace=h_margin/cell_width, hspace=v_margin/cell_height)

    if dstfile:
        plt.savefig(dstfile)
    
    plt.show()
    
def demo_plot_figures():
    # Example usage
    X = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],  # Multiple datasets for subplot 1
         [[1, 2, 3]]]  # Single dataset for subplot 2
    Y = [[[4, 5, 6], [7, 8, 9], [1, 4, 2]],  # Multiple datasets for subplot 1
         [[4, 5, 6]]]  # Single dataset for subplot 2
    xlabels = ['X1', 'X2']
    ylabels = ['Y1', 'Y2']
    titles = ['Plot 1', 'Plot 2']
    fmts = [['-o', '--s', ':^'],  # Formats for each line in subplot 1
            ['-o']]  # Format for the single line in subplot 2
    grid = [True, False]  # Grid settings for each subplot
    solid_markers = [[False, True, False], [True]]  # Solid/hollow marker settings for each curve
    legends = [['Curve 1', 'Curve 2', 'Curve 3'], None]  # Legends for each subplot (None for the second subplot)

    plot_figures(X,Y,xlabels=xlabels,ylabels=ylabels,titles=titles,
                ncol=2,cell_width=4,cell_height=3,h_margin=0.8,v_margin=0.5,
                fmts=fmts, grid=grid, solid_markers=solid_markers,
                dstfile = r'plot.png')

def demo_plot_2d_maps():
    # Example usage
    X = [np.random.rand(10, 20), np.random.rand(15, 15)]  # List of 2D data
    titles = ['Map 1', 'Map 2']
    colorbars = [True, False]  # Only show colorbar for the first subplot
    cmaps = ['hot', 'cool']  # Different colormaps for each subplot

    plot_2d_maps(X,titles=titles,ncol=2,cell_height=2,h_margin=0.5, 
                  colorbars=colorbars, cmaps=cmaps, show_axes=False,
                dstfile = '2D_maps.png')