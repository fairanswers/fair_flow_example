import pytest, fair_flow, fair_flow_example, demo
from dot_tools import parse
from dot_tools.dot_graph import SimpleGraph


@pytest.fixture()
def say():
    return fair_flow.Say("id22", "The Say Activity")

@pytest.fixture()
def sing():
    return fair_flow.Sing("id33", "The Sing Activity")

@pytest.fixture()
def process():
    two = fair_flow.Say("id22", "Say")
    three = fair_flow.Sing("id33", "Sing")
    three.add_parent(two.id)
    four = fair_flow.Say("id44", "Say")
    four.add_parent(two.id)
    five = fair_flow.Sing("id55", "Sing")
    five.add_parent(two.id)
    ps = fair_flow.Process("Process_Two")
    ps.activities.append(two)
    ps.activities.append(three)
    ps.activities.append(four)
    ps.activities.append(five)
    return ps

@pytest.fixture()
def good_dot_src():
    str='''
    digraph one {
  urgent [ name = "Always_True" state = "WAITING" returned = "Any" fillcolor=WHITE style=filled shape=ellipse]
  send_text [ name = "Random_True_False" state = "WAITING" returned = "Any" fillcolor=WHITE style=filled shape=ellipse]
  send_email [ name = "Always_False" state = "WAITING" returned = "Any" fillcolor=WHITE style=filled shape=ellipse]
  end [ name = "Say" state = "WAITING" returned = "Any" fillcolor=WHITE style=filled shape=ellipse]
  error [ name = "Say" state = "WAITING" returned = "Any" fillcolor=WHITE style=filled shape=ellipse]
  urgent -> send_email [label="False"]
  urgent -> send_text [label="True"]
  send_text -> end [label="True"]
  send_email -> end [label="True"]
  send_text -> error [label="False"]
  send_email -> error [label="False"]
}
    '''
    return str


def test_file_store(process):
    name=process.id
    data=process.to_dot()
    store=demo.file_dot_data_store('test_archive')
    # Cleanup from failed old test
    if len(store.list() )!= 0:
        store.delete('Process_Two')
    assert len(store.list() )==0
    out=store.save(process)
    loaded=store.load(name)
    #TODO: implement equals
    assert len(loaded.to_dot()) > 50 and len(process.to_dot()) > 50
    assert len(store.list())>0
    assert store.delete(loaded.id)
