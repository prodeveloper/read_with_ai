from collections import namedtuple


File = namedtuple("File", ["name", "stream","page_start","page_end"])
files_list =[
    File(
        name="designing_data_intensive.pdf", 
        stream="Data Engineering", 
        page_start=19, 
        page_end=700
    ),
    File(
        name="Designing_Distributed_Systems_Burns.pdf", 
        stream="System Design Interview", 
        page_start=36, 
        page_end=206
    ),
    File(
        name="System_design_interview_alex.pdf", 
        stream="System Design Interview", 
        page_start=8, 
        page_end=325
    ),
    File(
        name="cracking_coding_interview.pdf", 
        stream="coding", 
        page_start=35, 
        page_end=662
    ),

]
