# doc-flow
Сервис по обработке загружаемых данных администратором. То есть сделать API для приема документов со стороны фронтенда. При поступлении документа от зарегистрированного пользователя, необходимо уведомлять по почте администратора платформы. После того, как администратор подтвердил документ, отправлять письмо пользователю, который загружал документ. В Django admin добавить быстрые действия для подтверждения или отклоенения загруженных документов. Для рассылки необходимо использовать работу с очередью.