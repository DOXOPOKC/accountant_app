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
          v-spacer
          v-btn(
            v-if="packageActiveStatus"
            color="error"
            @click="DEACTIVATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
          )
            | Сделать неактивным
          v-btn(
            v-if="packageActiveStatus"
            class="ml-2"
            color="primary"
            @click="REGENERATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
          )
            | Перегенерировать
        v-card-text
          v-subheader(class="subtitle-1 black--text")
            a(:href="package.contract || ''" class="blue--text") Договор
          v-subheader(class="subtitle-1 black--text")
            a(:href="package.court_note || ''" class="blue--text") Претензия
          v-subheader(class="subtitle-1 black--text")
            a(:href="package.act_count || ''" class="blue--text") Акт сверки
          v-row(no-gutters)
            v-col(cols="4")
              v-list(rounded pa-0 max-width="400px")
                v-list-item-group(color="blue")
                  v-subheader Акты
                  v-list-item(
                    v-for="(file, i) in package.act_files"
                    :key="i"
                  )
                    v-list-item-content
                      v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                    v-list-item-icon
                      v-btn(fab :to="file.file_path || ''" color="blue" dark class="elevation-0" small)
                        v-icon mdi-download
            v-col(cols="4")
              v-list(rounded pa-0 max-width="400px")
                v-subheader Счета
                v-list-item(
                  v-for="(file, i) in package.count_files"
                  :key="i"
                )
                  v-list-item-content
                    v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                  v-list-item-icon
                    v-btn(fab :to="file.file_path || ''" color="blue" dark class="elevation-0" small)
                        v-icon mdi-download
            v-col(cols="4")
              v-list(rounded pa-0 max-width="400px")
                v-subheader Счета фактур
                v-list-item(
                  v-for="(file, i) in package.count_fact_files"
                  :key="i"
                )
                  v-list-item-content
                    v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                  v-list-item-icon
                    v-btn(fab :to="file.file_path || ''" color="blue" dark class="elevation-0" small)
                        v-icon mdi-download
</template>

<script>
import { mapState, mapActions } from 'vuex'
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
      package: state => state.packages.detail,
      packageActiveStatus: state => state.packages.detail.is_active
    })
  },
  mounted () {
    this.$nextTick(() => {
      this.$nuxt.$loading.start()
      setTimeout(() => this.$nuxt.$loading.finish(), 20000)
    })
  },
  methods: {
    ...mapActions({
      REGENERATE_PACKAGE: 'packages/REGENERATE_PACKAGE',
      DEACTIVATE_PACKAGE: 'packages/DEACTIVATE_PACKAGE'
    })
  }
}
</script>
