# Веб-приложение для онлайн-образования с автоматизированной проверкой знаний
Основное назначение платформы заключается в предоставлении возможности улучшить
процесс обучения, автоматизировав процесс проверки знаний и добавив командную работу в
процессе обучения. 

## Диаграмма вариантов использования
Перед началом разработки нам нужно понять какие действия пользователей нам нужно предусмотреть. Выделим три вида пользователей: Студент,
Администратор, Преподаватель. Студент может просмотреть информацию о
курсах, посмотреть доступные уроки и их материалы, посмотреть комментарии к нему и оставить свой. Также студент может решить тест, посмотреть
результаты тестов и посмотреть командный проект. Администратор может создать направление, объединив тематику курсов, создать курсы в направлениях
и предоставлять права доступа Преподавателям и Студентам. Преподаватель
может создавать уроки и тесты к ним, курсовые проекты, просматривать курсы
и результаты тестирования студентов. 

![Диаграмма вариантов использования](https://github.com/Afsent/education-platform/blob/master/schemas/Диаграмма%20вариантов%20использования.jpg)

## Диаграмма базы данных
На данном слайде из сущностей строится схема базы данных. Основными сущностями являются: пользователь, тест, направление курса, занятие,
вопрос, командный проект и комментарий. В качестве системы управления
базы данных используется MySQL.

![Диаграмма базы данных](https://github.com/Afsent/education-platform/blob/master/schemas/%D0%A1%D1%85%D0%B5%D0%BC%D0%B0%20%D0%B1%D0%B0%D0%B7%D1%8B%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.png)

## Граф состояний интерфейса 
Граф состояний интерфейса описывает переходы между страницами в
процессе обучения пользователем, показывая возможные пути при посещении
веб-приложения. Процесс обучения включает в себя следующие основные
страницы: регистрация или авторизация пользователя, главная страница и
меню, страница курса, урока, курсового проекта, а также страницы тестирования, вопросов и результатов тестирования. 

![Граф состояний интерфейса](https://github.com/Afsent/education-platform/blob/master/schemas/%D0%93%D1%80%D0%B0%D1%84%20%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B9%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81%D0%B0.jpg)

## Формы интерфейсов

### Форма регистрации пользователя
![Форма регистрации пользователя](https://github.com/Afsent/education-platform/blob/master/schemas/1.jpg)
### Страница урока и его материалов
![Страница урока и его материалов](https://github.com/Afsent/education-platform/blob/master/schemas/2.jpg)
### Вопросы при тестировании 
![Вопросы при тестировании](https://github.com/Afsent/education-platform/blob/master/schemas/3.jpg)
### Результаты тестирования 
![Результаты тестирования](https://github.com/Afsent/education-platform/blob/master/schemas/4.jpg)
