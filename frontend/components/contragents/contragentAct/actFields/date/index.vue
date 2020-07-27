<template lang="pug">
  v-col(cols="12")
      v-menu(
        ref="actDateMenu"
        v-model="actDateMenu"
        :close-on-content-click="false"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      )
        template(v-slot:activator="{ on, attrs }")
          v-text-field(
            v-model="actDate"
            label="Введите дату"
            prepend-icon="mdi-calendar-range"
            readonly
            v-bind="attrs"
            v-on="on"
          )
        v-date-picker(v-model="actDate" no-title scrollable)
          v-spacer
          v-btn(text color="primary" @click="actDateMenu = false") Закрыть
          v-btn(text color="primary" @click="$refs.actDateMenu.save(actDate)") Сохранить
</template>

<script>
export default {
  name: '',
  data: () => ({
    actDateMenu: false
  }),
  computed: {
    actDate: {
      set (actDate) {
        this.$store.commit('act/SET_ACT', { date: actDate })
      },
      get () {
        return this.$store.state.act.detail.date
      }
    }
  }
}
</script>
