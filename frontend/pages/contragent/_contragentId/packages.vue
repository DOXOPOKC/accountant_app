<template lang="pug">
  v-row(
    class="fill-height"
    justify="center"
    align="start"
    no-gutters
  )
    v-col(
      xs12
      sm8
      md6
    )
      v-card(
        flat
        exact
      )
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
            template(v-slot:top)
              v-toolbar(flat)
                v-toolbar-title Пакеты контрагента № {{ $route.params.contragentId }}
            template(v-slot:body="{ items }")
              tbody
                nuxt-link(tag="tr" :to="'/contragent/' + $route.params.contragentId + '/package/' + item.id + '/'" v-for="item in items" :key="item.name")
                  td(v-if="item.is_active")
                    v-chip(color="green" dark) {{ item.id }}
                  td(v-else color="red") {{ item.id }}
                  td {{ item.contragent }}
                  td {{ item.creation_date | dateFormat }}
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/packages'

export default {
  async asyncData ({ $axios, store, params }) {
    await store.dispatch(`packages/${types.FETCH_PACKAGES}`, params.contragentId)
  },
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
  methods: {
    ...mapActions([types.FETCH_PACKAGES])
  }
}
</script>
