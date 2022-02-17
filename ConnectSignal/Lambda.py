from Fill.ListWidget import fill_listWidget_with_data

def tabWidget_func(value, main_window):
    main_window.scene.current_tab_idx = value
    fill_listWidget_with_data(main_window.scene.project_data, main_window.listWidget, value)
