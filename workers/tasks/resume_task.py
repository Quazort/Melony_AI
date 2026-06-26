import json
from core.logger import get_logger
from workers.tasks.celery_schema import ResponseAISchema, ResponseSchema
from workers.tasks.general_agent import Agent
from workers.celery_config import app

logger = get_logger("celery-worker")


@app.task(name="resume_task", bind=True, retry_backoff=True, retry_jitter=True, max_retries=3, acks_late=True,
          reject_on_worker_lost=True)
def resume_processing(self, hr_requirements, resume):
    first_ai = Agent(
        role="Ты - профессиональный инструмент для анализа данных в сфере HR. Ты обязан строго следовать правилам и не придумывать факты.\n"
             "Тебе передаются требования к вакансии и резюме кандидата, которое нужно проверить.\n"
             "При проверке критически важно проверить ВСЕ резюме кандидата на наличие совпадений с требованиями даже если данные в конце резюме, в случае пропуска ты будешь оштрафована.\n"
             "В резюме могут быть ошибки, сокращения, названия вместо английского языка на русском, но ты должна корректно все обработать. \n"
             "На выходе ты должен вернуть СТРОГО валидный JSON-объект по следующему шаблону (соблюдай кавычки и типы данных):\n"
             "{\n"
             '  "full_name": "(Строка: Полное имя кандидата (ФИО))",\n'
             '  "date_of_birth": "(Строка: в формате ДД.ММ.ГГГГ или "не указано")",\n'
             '  "years_of_work": [Массив чисел: опыт в формате [год, месяц] строго числами только релевантный коммерческий доказанный опыт, если нет например года то пиши [0,2] если нет месяца то пиши [3,0] ],\n'
             '  "format_of_the_work": [Массив строк: в каком формате человек хочет работать. Всего есть 3 типа формата работ, выбирай и записывай строго из них "удаленно","на месте работодателя","гибрид"],\n'
             '  "skills": [Массив строк: записывай сюда точные строки из поля "requirements" только если умения человека строго подходят под эти требования],\n'
             '  "extra_skills": [Массив строк: записывай сюда точные строки из поля "extra_requirements" только если умения человека строго подходят под эти требования],\n'
             '  "matching_tasks": [Массив строк: записывай сюда точные строки из поля "tasks" только если человек строго занимался этими задачами],\n'
             '  "strengths": [Массив строк сильных сторон человека под эту вакансию],\n'
             '  "weaknesses": [Массив строк слабых сторон человека под эту вакансию]\n'
             "}\n"
             "Запрещено выводить любой текст, кроме этого JSON-объекта.\n"
             "За тобой наблюдают, любые ошибки и галлюцинации караются штрафами")
    second_ai = Agent(
        role="Ты - старший системный аудитор. Твоя задача - проверить качество работы младшей ИИ-модели.\n"
             "Ты получаешь: требования к вакансии, резюме человека и промежуточный JSON-результат, составленный первой моделью.\n"
             "Вот пример вывода json который должен быть:\n"
             "{\n"
             '  "full_name": "(Строка: Полное имя кандидата (ФИО))",\n'
             '  "date_of_birth": "(Строка: в формате ДД.ММ.ГГГГ или "не указано")",\n'
             '  "years_of_work": [Массив чисел: опыт в формате [год, месяц] строго числами только релевантный коммерческий доказанный опыт, если нет например года то пиши [0,2] если нет месяца то пиши [3,0] ],\n'
             '  "format_of_the_work": [Массив строк: в каком формате человек хочет работать. Всего есть 3 типа формата работ, выбирай и записывай строго из них "удаленно","на месте работодателя","гибрид"],\n'
             '  "skills": [Массив строк: записывай сюда точные строки из поля "requirements" только если умения человека строго подходят под эти требования],\n'
             '  "extra_skills": [Массив строк: записывай сюда точные строки из поля "extra_requirements" только если умения человека строго подходят под эти требования],\n'
             '  "matching_tasks": [Массив строк: записывай сюда точные строки из поля "tasks" только если человек строго занимался этими задачами],\n'
             '  "strengths": [Массив строк сильных сторон человека под эту вакансию],\n'
             '  "weaknesses": [Массив строк слабых сторон человека под эту вакансию]\n'
             "}\n"
             "При проверке критически важно проверить ВСЕ резюме кандидата на наличие совпадений с требованиями даже если данные в конце резюме, в случае пропуска ты будешь оштрафована.\n"
             "В резюме могут быть ошибки, сокращения, названия вместо английского языка на русском, но ты должна корректно все обработать. \n"
             "Ты обязан перепроверить:\n"
             "1. Соответствуют ли умения человека в поле 'skills' и 'extra_skills' требованиям к вакансии из поля 'requirements' и 'extra_requirements'?\n"
             "2. Проверь 'matching_tasks', в этом поле должны быть задачи которые реально выполнял человек и которые есть в требованиях к вакансии в поле 'tasks'"
             "3. Соответствует ли реальный опыт опыту в поле 'years_of_work' ?\n"
             "4. Не придумала ли первая модель сильные или слабые стороны кандидата?\n"
             "5. Является ли JSON строго валидным (двойные кавычки, правильные типы данных)?\n"
             "ТВОЙ ВЫХОД:\n"
             "Если промежуточный JSON идеален — верни его без изменений.\n"
             "Если в JSON есть ошибки, неверные оценки или галлюцинации — ИСПРАВЬ ИХ и верни исправленный, финальный валидный JSON в том же формате.\n"
             "Выводить разрешено ТОЛЬКО валидный JSON-объект. Любой текст вне JSON, комментарии или какие-то лишние данные запрещены и караются жестким штрафом."
    )
    try:
        logger.info("Первый ии начал работу")
        first_ai_result = ai_request(first_ai, f"ТРЕБОВАНИЯ---{hr_requirements} \n РЕЗЮМЕ---{resume}")
        logger.info("Первая ии отработала успешно")

        logger.info("Второй ии начал работу")
        second_ai_result = ai_request(second_ai,
                                      f"ТРЕБОВАНИЯ---{hr_requirements} \nРЕЗЮМЕ---{resume} \nРЕЗУЛЬТАТ ПЕРВОЙ ИИ---{first_ai_result}")
        logger.info("Вторая ии отработала успешно")

        score = score_points(hr_requirements, second_ai_result)
        final_report = ResponseSchema.model_validate({**second_ai_result, "points": score})
        logger.info(f"Final report: \n {final_report}")  # потом допилю фичу куда мне отправлять данные, пока в терминал
    except Exception as e:
        logger.info(f"Ошибка при генерации ответа: {e}")
        raise self.retry(exc=e)

    return "SUCCESS"


def ai_request(agent: Agent, text: str) -> dict | None:
    for i in range(2):
        try:
            appeal = agent.ai_generate_v2(text)
            response = ResponseAISchema.model_validate(json.loads(appeal.choices[0].message.content))
            return response.model_dump()
        except Exception as e:
            logger.warning(f"Ошибка ответа ИИ: {e}")
            if i == 1:
                raise e


def score_points(hr_requirements: dict, resume_dict: dict):
    score = 0
    extra_score = 0
    all_score_fields = {"max_score_years_of_work": 40, "max_score_requirements": 35, "max_score_format_of_the_work": 5,
                        "max_score_extra_requirements": 10, "max_score_tasks": 10}

    if not hr_requirements['extra_requirements']:
        extra_score += 10
        del all_score_fields["max_score_extra_requirements"]

    if not hr_requirements['tasks']:
        extra_score += 10
        del all_score_fields["max_score_tasks"]

    if extra_score:
        extra_score /= len(all_score_fields)
        for key, value in all_score_fields.items():
            all_score_fields[key] += extra_score

    if 'max_score_extra_requirements' in all_score_fields.keys():
        score += all_score_fields['max_score_extra_requirements'] if (len(
            hr_requirements['extra_requirements']) / 2) <= len(
            resume_dict['extra_skills']) else 0

    if 'max_score_tasks' in all_score_fields.keys():
        score += all_score_fields['max_score_tasks'] if (len(hr_requirements['tasks']) / 2) <= len(
            resume_dict['matching_tasks']) else 0

    if hr_requirements['years_of_work'] != 0:
        months_required = hr_requirements['years_of_work'] * 12
        resume_months = resume_dict['years_of_work'][0] * 12 + resume_dict['years_of_work'][1]

        if resume_months >= months_required:
            score += all_score_fields['max_score_years_of_work']
        else:
            score += resume_months * (all_score_fields['max_score_years_of_work'] / months_required)
    else:
        score += all_score_fields['max_score_years_of_work']

    score += all_score_fields['max_score_format_of_the_work'] if set(hr_requirements['format_of_the_work']) & set(
        resume_dict['format_of_the_work']) else 0

    if len(hr_requirements['requirements']) <= len(resume_dict['skills']):
        score += all_score_fields['max_score_requirements']
    else:
        one_score_hr_requirements = all_score_fields['max_score_requirements'] / len(hr_requirements['requirements'])
        score += one_score_hr_requirements * len(resume_dict['skills'])

    return round(score, 2)
