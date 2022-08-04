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


def scan_files(progress: Progress) -> t.Dict[str, ExamQuestion]:
    console.print(f'Scanning files in {os.getcwd()}...')
    questions = {}
    num_files = len(os.listdir())
    process_file_handle = progress.add_task(
        f'Process {num_files} files...', total=num_files)
    for file in os.listdir('.'):
        progress.update(process_file_handle, advance=1)
        if os.path.isfile(file):
            m = re.findall(r'^q([0-9]+).*\.txt$', file)
            if len(m) == 1:
                question_number = int(m[0])
                if question_number not in questions:
                    questions[question_number] = {
                        'question_number': question_number,
                        'type': ExamQuestionType.MCQ_SHORT_RESPONSE,
                        'files': []
                    }
                questions[question_number]['files'].append(file)
        elif os.path.isdir(file):
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
                questions[question_number]['files'].append(file)
    return questions


def initialise():
    progress = Progress()
    with progress:
        files = scan_files(progress=progress)
    console.print(f'Found {len(files.keys())} questions.')
    tb = Table()
    tb.add_column('Question')
    tb.add_column('Type')
    tb.add_column('Files')
    for question in sorted(files.values(), key=lambda x: x['question_number']):
        tb.add_row(str(question['question_number']),
                   ExamQuestionTypeName[question['type']],
                   ', '.join(question['files']))
    console.print(tb)
    pass
