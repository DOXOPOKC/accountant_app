<template lang="pug">
  v-col(cols="12")
    v-select(
      disabled
      item-text="class"
      item-value="value"
      v-model="klass"
      :items="classTypes"
      label="Класс контрагента"
    )
</template>

<script>
export default {
  data: () => ({
    classTypes: [
      { value: 0, class: '' },
      { value: 1, class: 'Юридическое лицо без договора' },
      { value: 2, class: 'Юридическое лицо с договором' },
      { value: 3, class: 'ИЖС без договора' },
      { value: 4, class: 'ИЖС с договором' },
      { value: 5, class: 'Физическое лицо' }
    ]
  }),
  computed: {
    klass: {
      set (klass) {
        this.$store.commit('contragents/SET_CONTRAGENT', { klass })
      },
      get () {
        return this.$store.state.contragents.detail.klass
      }
    }
  }
}
// disabled
</script>
