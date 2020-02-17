import Vue from 'vue'
import { format } from 'date-fns'

Vue.filter('dateFormat', function dateFormat (value) {
  if (value) {
    return format(new Date(value), 'dd/MM/yyyy')
  }
  return '(n/a)'
})
