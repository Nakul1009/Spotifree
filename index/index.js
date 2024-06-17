function myFunction(a){
    alert(a);
    var python_process = spawner('python', ['index.py',a]);
    alert(python_process);
}