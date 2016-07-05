from boto.mturk.connection import MTurkConnection
from boto.mturk.question import QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer
from boto.mturk.qualification import Qualifications, Requirement
import csv, random

ACCESS_ID =''
SECRET_KEY = ''
HOST = 'mechanicalturk.sandbox.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

title = 'Map images to emotions'
description = ('Given an image identify what emotion'
               ' the image depicts and whether the ANP is correct')
keywords = 'image, emotions, ANP'

ratings =[('Ecstacy','1'),
          ('Joy','2'),
          ('Serenity','3'),
          ('Admiration','4'),
          ('Trust','5'),
          ('Acceptance','6'),
          ('Terror','7'),
          ('Fear','8'),
          ('Apprehension','9'),
          ('Amazement','10'),
          ('Surprise','11'),
          ('Distraction','12'),
          ('Grief','13'),
          ('Sadness','14'),
          ('Pensiveness','15'),
          ('Loathing','16'),
          ('Disgust','17'),
          ('Boredom','18'),
          ('Rage','19'),
          ('Anger','20'),
          ('Annoyance','21'),
          ('Vigilance','22'),
          ('Anticipation','23'),
          ('Interest','24')]

binaryAnswer =[('Yes','1'),
               ('No','0')]

ANP_dict = dict()
f = open('testfile.csv')
csv_f = csv.reader(f)

for row in csv_f:
    if row[0] in ANP_dict:
        ANP_dict[row[0]].add(row[1])
    elif row[0] not in ANP_dict:
        ANP_dict[row[0]] = set()
        ANP_dict[row[0]].add(row[1])

#---------------  CREATE QUALIFICATION -------------
overview = Overview()
overview.append_field("Title", "Qualification Test")
q1_overview = Overview()
with open('QualificationInstructions.html') as f:
    instructions="\n".join(line.strip() for line in f)
q1_overview.append(FormattedContent(instructions))

with open('q1.html') as f:
    img="\n".join(line.strip() for line in f)
q1_overview.append(FormattedContent(img))

qc1 = QuestionContent()
qc1.append_field('Title','What emotion does this image depicts?')

fta1 = SelectionAnswer(min=1, max=24,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

q1 = Question(identifier='question1',
              content=qc1,
              answer_spec=AnswerSpecification(fta1),
              is_required=True)

q2_overview = Overview()

with open('q2.html') as f:
    img="\n".join(line.strip() for line in f)
q2_overview.append(FormattedContent(img))

qc2 = QuestionContent()
qc2.append_field('Title','What emotion does this image depicts?')

fta2 = SelectionAnswer(min=1, max=24,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

q2 = Question(identifier='question2',
              content=qc2,
              answer_spec=AnswerSpecification(fta2),
              is_required=True)

q3_overview = Overview()

with open('q3.html') as f:
    img="\n".join(line.strip() for line in f)
q3_overview.append(FormattedContent(img))

qc3 = QuestionContent()
qc3.append_field('Title','What emotion does this image depicts?')

fta3 = SelectionAnswer(min=1, max=24,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

q3 = Question(identifier='question3',
              content=qc3,
              answer_spec=AnswerSpecification(fta3),
              is_required=True)

q4_overview = Overview()

with open('q4.html') as f:
    img="\n".join(line.strip() for line in f)
q4_overview.append(FormattedContent(img))

qc4 = QuestionContent()
qc4.append_field('Title','What emotion does this image depicts?')

fta4 = SelectionAnswer(min=1, max=24,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

q4 = Question(identifier='question4',
              content=qc4,
              answer_spec=AnswerSpecification(fta4),
              is_required=True)

q5_overview = Overview()

with open('q5.html') as f:
    img="\n".join(line.strip() for line in f)
q5_overview.append(FormattedContent(img))

qc5 = QuestionContent()
qc5.append_field('Title','What emotion does this image depicts?')

fta5 = SelectionAnswer(min=1, max=24,style='checkbox',
                      selections=ratings,
                      type='text',
                      other=False)

q5 = Question(identifier='question5',
              content=qc5,
              answer_spec=AnswerSpecification(fta5),
              is_required=True)

ques_form = QuestionForm()
ques_form.append(overview)
ques_form.append(q1_overview)
ques_form.append(q1)
ques_form.append(q2_overview)
ques_form.append(q2)
ques_form.append(q3_overview)
ques_form.append(q3)
ques_form.append(q4_overview)
ques_form.append(q4)
ques_form.append(q5_overview)
ques_form.append(q5)

with open('AnswerKey.xml') as f:
    ans_key="\n".join(line.strip() for line in f)

qual_name="Qualification_31"
qual_type=mtc.create_qualification_type(name=qual_name,
                                        description="A qualification for our HITs",
                                        status="Active",
                                        retry_delay=60*5,
                                        keywords=keywords,
                                        test=ques_form,
                                        answer_key=ans_key,
                                        test_duration=1800)

qual_id = qual_type[0].QualificationTypeId

req = Requirement(qualification_type_id=qual_id,
                  comparator="GreaterThanOrEqualTo",
                  integer_value=3)

# Add qualification test
qual = Qualifications()
qual.add(req)

#---------------  BUILD OVERVIEW -------------------
overview1 = Overview()
with open('Instructions.html') as f:
    instructions="\n".join(line.strip() for line in f)
overview1.append(FormattedContent(instructions))

for ANP in ANP_dict:
    overview2 = Overview()
    for i in range(0, 2):
        url = random.sample(ANP_dict[ANP],5)
        img = '<table>\n'
        img += '<tr>\n'
        for j in range(0,5):
            img_str = '<td><img src="'
            img_str += url[j]
            img_str += '" alt="Test Image" width="128" height="128"/></td>\n'
            img += img_str
        img += '</tr>\n'
        img += '</table>'
        overview2.append(FormattedContent(img))

    anp = ANP.split('_')
    adj = anp[0]
    noun = anp[1]
#---------------  BUILD QUESTION 1 -------------------
    qc1 = QuestionContent()
    qc1.append_field('Title','What are the emotions expressed by the ANP '+ adj + ' ' + noun +' and the images related to the ANP shown above?')

    fta1 = SelectionAnswer(min=1, max=24,style='checkbox',
                        selections=ratings,
                        type='text',
                        other=False)

    q1 = Question(identifier=ANP,
                content=qc1,
                answer_spec=AnswerSpecification(fta1),
                is_required=True)

    #--------------- BUILD THE QUESTION FORM -------------------
    question_form = QuestionForm()
    question_form.append(overview1)
    question_form.append(overview2)
    question_form.append(q1)

    #--------------- CREATE THE HIT -------------------
    mtc.create_hit(questions=question_form,
                max_assignments=1,
                title=title,
                description=description,
                keywords=keywords,
                duration = 60*5,
                reward=0.05,
                qualifications=qual)

print 'HITs posted successfully'
