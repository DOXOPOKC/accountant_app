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
        v-card-title(class="headline font-weight-light px-10")
          | Пакет № {{ package.id }}
        v-card-text
          v-subheader(class="subtitle-1 black--text")
            a(:href="'http://jud-module.lf.ru' + package.contract" class="blue--text") Договор
          v-subheader(class="subtitle-1 black--text")
            a(:href="'http://jud-module.lf.ru' + package.court_note" class="blue--text") Претензия
          v-subheader(class="subtitle-1 black--text")
            a(:href="'http://jud-module.lf.ru' + package.act_count" class="blue--text") Акт сверки
          v-list
            v-subheader(class="subtitle-1 black--text") Акты
            v-list-item(
              v-for="(file, i) in package.act_files"
              :key="i"
            )
              v-list-item-content
                v-list-item-title
                  a(v-text="file.file_name" :href="'http://jud-module.lf.ru' + file.file_path" class="blue--text")

          v-list
            v-subheader Счета
            v-list-item(
              v-for="(file, i) in package.count_files"
              :key="i"
            )
              v-list-item-content
                v-list-item-title
                  a(v-text="file.file_name" :href="'http://jud-module.lf.ru' + file.file_path" class="blue--text")

          v-list
            v-subheader Счета фактур
            v-list-item(
              v-for="(file, i) in package.count_fact_files"
              :key="i"
            )
              v-list-item-content
                v-list-item-title
                  a(v-text="file.file_name" :href="'http://jud-module.lf.ru' + file.file_path" class="blue--text")
</template>

<script>
import { mapState } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'
import { types } from '~/store/packages'

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch(`packages/${types.FETCH_PACKAGE}`, { contragentId: params.contragentId, packageId: params.id })
  },
  data: () => ({}),
  computed: {
    ...mapState({
      package: state => state.packages.detail
    }),
    panels () {
      return [...Array(this.contragentInfo.length).keys()]
    }
  },
  methods: {}
}
</script>
