<template lang="pug">
  v-card(
    v-if="packages.length"
    flat
    exact
    class="fill-height"
  )
    v-card-title(class="headline font-weight-light")
      | Пакеты контрагента № {{ $route.params.id }}
    v-card-text(class="pa-0")
      v-data-table(
        :headers="headers"
        :items="packages"
        item-key="id"
        class="elevation-0"
        sort-by="id"
        sort-desc
        disable-pagination
        disable-filtering
        calculate-widths
        hide-default-footer
      )
        template(v-slot:body="{ items }")
          tbody
            nuxt-link(tag="tr" :to="'/contragent/' + item.contragent + '/package/' + item.id + '/'" v-for="item in items" :key="item.name")
              td(v-if="item.is_active")
                v-chip(color="green" dark) {{ item.id }}
              td(v-else color="red") {{ item.id }}
              td {{ item.contragent }}
              td {{ item.creation_date | dateFormat }}
  v-card(
    v-else
    class="mx-auto my-0"
    max-width="250"
    color="warning"
    dark
    tile
  )
    v-card-text(dark class="my-4 text-center title font-weight-regular") Сгенерируйте пакет!
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/packages'

export default {
  data: () => ({
    headers: [
      {
        text: 'Номер',
        align: 'left',
        sortable: false,
        value: 'id'
      },
      { text: 'Контрагент', value: 'contragent' },
      { text: 'Дата создания', value: 'creation_date' }
      // { text: 'Действия' }
      // Дата последнего платежа
      // Ответственное лицо
    ]
  }),
  computed: {
    ...mapState({
      packages: state => state.packages.list
    })
  },
  async created () {
    await this.FETCH_PACKAGES(this.$route.params.contragentId)
  },
  methods: {
    ...mapActions('packages', [types.FETCH_PACKAGES])
  }
}
</script>
