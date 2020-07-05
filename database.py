
from tkinter import *
from PIL import Image,ImageTk
import sqlite3



root=Tk()
root.title('gui for db')
root.iconbitmap('unnamed.png')
root.geometry("400x400")



conn=sqlite3.connect('applications_issues.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS issues(
         name text,
         app text,
         issue text,
         solution text
         )""")


def update():
    conn=sqlite3.connect('applications_issues.db')
    c=conn.cursor()
    record_id=delete_box.get()
#    c.execute("""UPDATE issues SET
#    name=:name,
#    app=:app;
#    issue=:issue,
#    solution=:solution,
#
#    WHERE oid=:oid""",
#    {'name':name_editor.get(),
#    'app':app_editor.get(),
#    'issue':issue_editor.get(),
#    'solution':solution_editor.get(),
#    #'oid':record_id
#    })
    c.execute("UPDATE issues SET name = ?, app = ?, issue = ?, solution = ? WHERE oid = ?", (name_editor, app_editor, issue_editor, solution_editor, record_id))
    conn.commit()
    conn.close()
    editor.destroy()


def edit():
    global editor
    editor=Tk()
    editor.title('Update a record')
    editor.iconbitmap('unnamed.png')
    editor.geometry("400x600")
    
    
    conn=sqlite3.connect('applications_issues.db')
    c=conn.cursor()
    record_id=delete_box.get()
    c.execute("SELECT * FROM issues where oid="+record_id)
    records=c.fetchall()

    global name_editor
    global app_editor
    global issue_editor
    global solution_editor
    
    name_editor=Entry(editor,width=30)
    name_editor.grid(row=0,column=1,padx=20,pady=(10,0))

    app_editor=Entry(editor,width=30)
    app_editor.grid(row=1,column=1,padx=20)

    issue_editor=Entry(editor,width=30)
    issue_editor.grid(row=2,column=1,padx=20)

    solution_editor=Entry(editor,width=30)
    solution_editor.grid(row=3,column=1,padx=20)
    
    name_label=Label(editor,text='Name')
    name_label.grid(row=0,column=0,pady=(10,0))

    app_label=Label(editor,text='app')
    app_label.grid(row=1,column=0)

    issue_label=Label(editor,text='issue')
    issue_label.grid(row=2,column=0)

    solution_label=Label(editor,text='solution')
    solution_label.grid(row=3,column=0)

    for record in records:
        name_editor.insert(0,record[0])
        app_editor.insert(0,record[1])
        issue_editor.insert(0,record[2])
        solution_editor.insert(0,record[3])

    save_button=Button(editor,text="Save Record",command=update)
    save_button.grid(row=4,column=0,columnspan=2,pady=10,padx=10,ipadx=143)


def delete():
    conn=sqlite3.connect('applications_issues.db')
    c=conn.cursor()
    c.execute("DELETE FROM issues WHERE oid="+delete_box.get())
    conn.commit()
    conn.close()


def submit():
    conn=sqlite3.connect('applications_issues.db')
    c=conn.cursor()
    c.execute("INSERT INTO issues VALUES (:name,:app,:issue,:solution)",
             {
                 'name':name.get(),
                 'app':app.get(),
                 'issue':issue.get(),
                 'solution':solution.get(),
             })
    conn.commit()
    conn.close()
    name.delete(0,END)
    app.delete(0,END)
    issue.delete(0,END)
    solution.delete(0,END)


def query():
    conn=sqlite3.connect('applications_issues.db')
    c=conn.cursor()
    c.execute("SELECT *, oid FROM issues")
    records=c.fetchall()
    print(records)
    print_records=''
    for record in records:
        print_records+=str(record[0]) + " "+str(record[1]) + " "+str(record[2]) + " "+str(record[3]) + " "+str(record[4])+"\n"
    query_label=Label(root,text=print_records)
    query_label.grid(row=6,column=0,columnspan=2)
    conn.commit()
    conn.close()


name=Entry(root,width=30)
name.grid(row=0,column=1,padx=20,pady=(10,0))

app=Entry(root,width=30)
app.grid(row=1,column=1,padx=20)

issue=Entry(root,width=30)
issue.grid(row=2,column=1,padx=20)

solution=Entry(root,width=30)
solution.grid(row=3,column=1,padx=20)

delete_box=Entry(root,width=30)
delete_box.grid(row=7,column=1)

name_label=Label(root,text='Name')
name_label.grid(row=0,column=0,pady=(10,0))

app_label=Label(root,text='app')
app_label.grid(row=1,column=0)

issue_label=Label(root,text='issue')
issue_label.grid(row=2,column=0)

solution_label=Label(root,text='solution')
solution_label.grid(row=3,column=0)

delete_box_label=Label(root,text="Select ID")
delete_box_label.grid(row=7,column=0)

submit_button=Button(root,text="Add Record To Database",command=submit)
submit_button.grid(row=4,column=0,columnspan=2,pady=10,padx=10,ipadx=100)

query_button=Button(root,text="Show Records",command=query)
query_button.grid(row=5,column=0,columnspan=2,pady=10,padx=10,ipadx=137)

delete_button=Button(root,text="Delete Record",command=delete)
delete_button.grid(row=8,column=0,columnspan=2,pady=10,padx=10,ipadx=136)

edit_button=Button(root,text="Update Record",command=edit)
edit_button.grid(row=9,column=0,columnspan=2,pady=10,padx=10,ipadx=143)


conn.commit()
conn.close()
root.mainloop()

