import { extend, localize } from 'vee-validate'
import { required } from 'vee-validate/dist/rules'

import ru from 'vee-validate/dist/locale/ru.json'

extend('required', {
  ...required,
  message: 'Поле обязательно для заполнения'
})

localize('ru', {
  ...ru
})
