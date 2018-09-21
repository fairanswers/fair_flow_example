import fair_flow, fair_flow_example
from flask import Flask, request, send_from_directory, render_template
import os, time
app = Flask(__name__)


# Details around storing dot files to disk.

# Example superclass that implements CRUD.  Reference this class to be able to switch out.
class dot_data_store():

    def save(self, dot):
        pass

    def load(self, id):
        pass

    def delete(self, id):
        pass

    def list(self):
        pass

# Example concrete class that implements generic super class
class file_dot_data_store(dot_data_store):
    store_dir=""
    extention=".dot"

    def filename_from_id(self, id):
        filename = self.store_dir + os.sep + id + self.extention
        return filename

    def __init__(self, dir=os.getcwd()+os.sep+"dot_archive"):
        self.store_dir=dir
        if not os.path.exists(self.store_dir):
            os.makedirs(self.store_dir)
        if not os.access(self.store_dir, os.W_OK):
            raise IOError("Can't write to archive directory "+self.store_dir)

    def save(self, dot):
        filename=self.filename_from_id(dot.id)
        with open(filename, 'w') as f:
            f.write(dot.to_dot() )
            return dot

    def load(self, id):
        filename = self.filename_from_id(id)
        with open(filename) as f:
            dot=f.read()
        ps= fair_flow.Process.parse(dot)
        return ps

    def delete(self, id):
        filename = self.filename_from_id(id)
        os.remove(filename)
        return True

    def list(self):
        cont=os.listdir(self.store_dir)
        return cont

store=file_dot_data_store()


@app.route('/health_check')
def health_check():
    return "OK\n\n"

# @app.route('/flow', methods = ['GET', 'PUT', 'POST', 'DELETE'])
# def flow():
#     return request.method+" OK\n\n"

@app.route("/run", methods = ['POST'])
def run():
    file = request.data
    ps = fair_flow.Process.parse(file)
    runner = fair_flow.FlexibleJobRunner()
    filename="JOB-"+time.strftime("%Y-%m-%d_%H_%M_%S")
    job = ps.createJob(filename)
    runner.execute_job(job)
    return job.to_dot()

@app.route("/step", methods = ['POST'])
def step():
    file = request.data
    ps = fair_flow.Process.parse(file)
    runner = fair_flow.FlexibleJobRunner()
    filename="JOB-"+time.strftime("%Y-%m-%d_%H_%M_%S")
    job = ps.createJob(filename)
    runner.execute_job(job, True)
    return job.to_dot()

@app.route("/flow/<string:id>/", methods = ['GET', 'POST', 'DELETE'])
@app.route("/flow/", defaults={'id': None} , methods = ['GET'])
def dot_edit(id=None):
    if request.method == 'GET':
        if id == None:
            list=store.list()
            page=jsonify(list)
            return page
        file=store.load(id)
        return file.to_dot()
    if request.method == 'POST':
        file=request.data
        ps = Process.parse(file)
        store.save(ps)
        return ps.to_dot()
    if request.method == 'DELETE':
        store.delete(str(id))
        return "Ok"

@app.route('/')
def root():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
