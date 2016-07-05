from boto.mturk.connection import MTurkConnection
from itertools import chain
from datetime import datetime
import csv

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def formAns(ans_obj):
    ans_tuple = map(lambda a: (a.qid, a.fields), ans_obj)
    return dict(ans_tuple)

def parseAnswer(form, ANP_set):
    # Create a dictionary to hold form responses
    form_dict = {}

    # Stick form response in a dict
    for a in form.answers:
        form_ans = formAns(a)
        for r in form_ans.keys():
            form_dict[r] = list()
            for value in form_ans.values():
                form_dict[r].append(value)

    # Form responses where no data is recorded will have a None value
    return form_dict

def reviewAssignment(a, ANP_set, mturk=None, auto_approve=True, redownload=False):
    answer_list = list()
    aid = a.AssignmentId
    status = a.AssignmentStatus
    if status == "Submitted":
        if auto_approve:
            mtc.approve_assignment(aid)
        answer_list.append(parseAnswer(a, ANP_set))
    if a.AssignmentStatus == "Approved" and redownload:
        answer_list.append(parseAnswer(a, ANP_set))
    return answer_list

if __name__ == '__main__':

    #emotions
    emotions=['Ecstacy',
              'Joy',
              'Serenity',
              'Admiration',
              'Trust',
              'Acceptance',
              'Terror',
              'Fear',
              'Apprehension',
              'Amazement',
              'Surprise',
              'Distraction',
              'Grief',
              'Sadness',
              'Pensiveness',
              'Loathing',
              'Disgust',
              'Boredom',
              'Rage',
              'Anger',
              'Annoyance',
              'Vigilance',
              'Anticipation',
              'Interest']

    ratings = range(1,25)

    d = dict(zip(emotions, ratings))

    # File path to downloads
    res_dir = "results/sandbox/"

    # Record start time
    start_time = datetime.now().strftime("%s")

    ACCESS_ID =''
    SECRET_KEY = ''
    HOST = 'mechanicalturk.sandbox.amazonaws.com'

    mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                          aws_secret_access_key=SECRET_KEY,
                          host=HOST)

    ANP_set = set()
    f = open('testANP.csv')
    csv_f = csv.reader(f)

    for row in csv_f:
        ANP_set.add(row[0])

    ANP_set.add('design')

    # Download reviewable HITs
    reviewable_assignments = list()
    hits = mtc.get_all_hits()
    hit_list = map(lambda h: h, hits)
    for h in hit_list:
        max_page = False
        m = 10
        p = 1
        while not max_page:
            assignments = mtc.get_assignments(h.HITId, page_size=m, page_number=p)
            if len(assignments) > 0:
                reviewable_assignments.extend(assignments)
                if(len(assignments) < m):
                    max_page = True
                else:
                    p += 1
            else:
                max_page =True

    # Review assignments
    response_list = list()
    for a in reviewable_assignments:
        submitted_work = reviewAssignment(a, ANP_set, mtc, redownload=True)
        if len(submitted_work) > 0:
            response_list.append(submitted_work)
    responses = list(chain.from_iterable(response_list))

    anp_keys = map(lambda i: i,  ANP_set)
    anp_dict = dict.fromkeys(anp_keys, None)

    for ans_tuple in responses:
        cur_key = ans_tuple.keys()
        cur_val = ans_tuple.values()
        if cur_key[0] in anp_dict:
            anp_dict[cur_key[0]] = zerolistmaker(len(emotions))
            for value in cur_val[0][0]:
                val = int(value)
                anp_dict[cur_key[0]][val-1] += 1 

    anp_emotions_list = emotions
    anp_emotions_list.insert(0, 'ANP')

    # Output file, name simply based on the time it is created
    if len(responses) > 0:
        f = res_dir+start_time+".csv"
        with open(f,'wb') as fp:
            print >>fp, ", ".join(anp_emotions_list)
            w = csv.writer(fp)
            for k, v in anp_dict.iteritems():
                w.writerow([k] + v)

        fp.close()
