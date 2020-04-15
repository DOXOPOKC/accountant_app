<template lang="pug">
  v-col(cols="12")
    v-select(
      readonly
      v-model="klass"
      :items="classTypes"
      label="Класс контрагента"
    )
</template>

<script>
export default {
  data: () => ({
    classTypes: [
      { value: 0, text: '' },
      { value: 1, text: 'Юридическое лицо без договора' },
      { value: 2, text: 'Юридическое лицо с договором' },
      { value: 3, text: 'ИЖС без договора' },
      { value: 4, text: 'ИЖС с договором' },
      { value: 5, text: 'Физическое лицо' }
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
