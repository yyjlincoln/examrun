import re
from rich.progress import Progress
import typing as t
import enum
from rich.table import Table
import os
from globals import console


class ExamQuestionType(enum.Enum):
    MCQ_SHORT_RESPONSE = 1
    PROGRAMMING_QUESTION = 2


ExamQuestionTypeName = {
    ExamQuestionType.MCQ_SHORT_RESPONSE: 'MCQ / Short Response',
    ExamQuestionType.PROGRAMMING_QUESTION: 'Programming Question'
}


class ExamQuestion(t.TypedDict):
    question_number: int
    type: ExamQuestionType
    files: t.List[str]


def scan_files(root=os.getcwd(),
               path='',
               questions: t.Dict[int, ExamQuestion] = {},
               currentQuestionNumber=None) -> t.Dict[str, ExamQuestion]:
    console.print(f'Scanning files in {os.path.join(root, path)}...')
    for file in os.listdir(os.path.join(root, path)):
        fileReal = os.path.join(root, path, file)
        if currentQuestionNumber is None:
            if os.path.isfile(fileReal):
                m = re.findall(r'^q([0-9]+).*\.txt$', file)
                if len(m) == 1:
                    question_number = int(m[0])
                    if question_number not in questions:
                        questions[question_number] = {
                            'question_number': question_number,
                            'type': ExamQuestionType.MCQ_SHORT_RESPONSE,
                            'files': []
                        }
                    questions[question_number]['files'].append(fileReal)
            elif os.path.isdir(fileReal):
                m = re.findall(r'^q([0-9]+)$', file)
                if not m:
                    continue
                if len(m) == 1:
                    question_number = int(m[0])
                    if question_number not in questions:
                        questions[question_number] = {
                            'question_number': question_number,
                            'type': ExamQuestionType.PROGRAMMING_QUESTION,
                            'files': []
                        }
                    questions[question_number]['files'].append(fileReal)
                    scan_files(root, fileReal,
                               questions, question_number)
        else:
            if os.path.isfile(fileReal):
                questions[currentQuestionNumber]['files'].append(fileReal)
            elif os.path.isdir(fileReal):
                scan_files(root, fileReal,
                           questions, currentQuestionNumber)

    return questions


def scan():
    progress = Progress()
    with progress:
        files = scan_files()
    console.print(f'Found {len(files.keys())} questions.')
    tb = Table(show_lines=True)
    tb.add_column('Question')
    tb.add_column('Type')
    tb.add_column('Files Found')
    for question in sorted(files.values(), key=lambda x: x['question_number']):
        question_short_files = [f.split(os.getcwd()+"/")[-1]
                                for f in question['files']]
        tb.add_row(str(question['question_number']),
                   ExamQuestionTypeName[question['type']],
                   '\n'.join(question_short_files))
    console.print(tb)
    return files
