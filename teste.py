from tkinter import *
from tkinter import ttk

# to be used by TrClicked Function for helping clear older clicked items
global clicked_queue
clicked_queue = []  # last 3 items


def onTripleClick(event):
    global clicked_queue
    # 'trClicked'+iid  - a unique tag for each item

    # the iid (string) of the item that currently has focus, or '' if no item has focus
    current_item_iid = event.widget.focus()
    if not current_item_iid:
        return
    print(event.widget.item(current_item_iid))
    print("current:", current_item_iid)  # iid=count

    if clicked_queue:
        # get the previous item, the last one in the queue
        prev_item_iid = clicked_queue[-1]
        print("prev item:", prev_item_iid)

        if prev_item_iid == current_item_iid:
            return

        tree.tag_configure('trClicked' + prev_item_iid, background='pink',
                           foreground='black', font=('Courier', 8, 'normal', 'roman'))

    tree.tag_configure('trClicked' + current_item_iid, background='light green',
                       foreground='black', font=('Helvetica', 8, 'bold', 'italic'))

    # add current item to the right side of the queue
    clicked_queue.append(current_item_iid)
    print("new prev item:", current_item_iid)

    if len(clicked_queue) == 3:
        # get and remove an element from the left side of the queue
        prev_prev_item_iid = clicked_queue[0]
        clicked_queue.remove(prev_prev_item_iid)

        if prev_prev_item_iid == current_item_iid:
            return

        # return to the default style
        tree.tag_configure('trClicked' + prev_prev_item_iid, background='white',
                           foreground='black', font=('Courier', 8, 'normal', 'roman'))


# Create main root object of TK class
root = Tk()
root.title('MyTreeview')
root.geometry("700x500")

# create a consistent style for the background and font
style = ttk.Style()
style.configure('Treeview', background='white', foreground='black', font=('Courier', 40, 'normal', 'roman'), rowheight=60)

# create frame to house treeview AND scrollbar
frame = Frame(root)
frame.pack(pady=5)

tree = ttk.Treeview(frame, height=20, selectmode="browse")
tree.pack(side=LEFT)
tree['columns'] = ("Column1", "Column2", "Column3")

# Format Columns
tree.column("#0", width=10, minwidth=10)  # this is where the plus icon will live
tree.column("Column1", anchor=W, width=150)
tree.column("Column2", anchor=W, width=300)
tree.column("Column3", anchor=W, width=120)

# Create headings
tree.heading("#0", text="", anchor=W)
tree.heading("Column1", text="Column1", anchor=W)
tree.heading("Column2", text="Column2", anchor=W)
tree.heading("Column3", text="Column3", anchor=W)

rows = [
    ['TopMostParent1', '2ndParent-ColE', 'ColF-3rdParent'],
    ['TopMostParent2', '5thParent-ColE', 'ColF-1stParent'],
    ['TopMostParent3', '4thParent-ColE', 'ColF-2ndParent'],
    ['TopMostParent4', '2ndParent-ColE', 'ColF-3rdParent'],
    ['TopMostParent4', '4thParent-ColE', 'ColF-1stParent'],
    ['TopMostParent6', '3rdParent-ColE', 'ColF-2ndParent'],
    ['TopMostParent5', '3rdParent-ColE', 'ColF-1stParent'],
    ['TopMostParent4', '3rdParent-ColE', 'ColF-3rdParent'],
    ['TopMostParent2', '3rdParent-ColE', 'ColF-3rdParent']
]
count = 1  # <- start at 1 or set iid=str(count), otherwise iid=0 will default to "I001"
for row in rows:
    tree.insert(parent='', index='end', iid=count, text='', tags=('trClicked' + str(count),),
                values=(row[0], row[1], row[2]))
    count += 1

tree.bind("<Triple-1>", onTripleClick)

root.mainloop()