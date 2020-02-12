<template lang="pug">
  v-col(cols="12")
    v-select(
      disabled
      item-text="text"
      item-value="value"
      v-model="is_func"
      :items="statusList"
      label="Статус"
    )
</template>

<script>
export default {
  data: () => ({
    statusList: [
      { text: 'Активен', value: true },
      { text: 'Неактивен', value: false }
    ]
  }),
  computed: {
    is_func: {
      set (isFunc) {
        this.$store.commit('contragents/SET_CONTRAGENT', { is_func: isFunc })
      },
      get () {
        return this.$store.state.contragents.detail.is_func
      }
    }
  }
}
// disabled  ? 'Активен': 'Неактивен'
</script>
