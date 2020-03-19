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
            class="custom-transform-class text-none"
            color="error"
            @click="DEACTIVATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
          )
            | Сделать неактивным
          v-btn(
            v-if="packageActiveStatus"
            class="ml-2 custom-transform-class text-none"
            color="primary"
            @click="REGENERATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
          )
            | Перегенерировать
          v-btn(
            v-if="packageActiveStatus"
            outlined
            class="ml-2 custom-transform-class text-none"
            color="primary"
            @click="packageDialogState = true"
          )
            | Добавить файл
        v-card-text
          v-dialog(
            v-model="packageDialogState"
            persistent
            max-width="600px"
          )
            v-card(outlined)
              v-card-title
                span(class="headline") Добавление файла
              v-card-text
                v-container(px-0 pb-0)
                  v-row(no-gutters)
                    v-col(cols="12")
                      VueFileAgent(
                        ref="vueFileAgent"
                        v-model="filesDataForUpload"
                        :theme="'list'"
                        :maxFiles="1"
                        :multiple="true"
                        :deletable="true"
                        :compact="true"
                        :helpText="'Загрузите свой файл'"
                        :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                        @delete="fileDeleted($event)"
                      )
                      small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
              v-card-actions
                v-spacer
                v-btn(color="blue darken-1" text @click="packageDialogState = false") Закрыть
                v-btn(color="blue darken-1" text @click="upload") Отправить
          v-subheader(class="subtitle-1 black--text" v-for="file in package['single_files']")
            a(:href="file.file_path" class="blue--text") {{ file.file_type.doc_type }}
          v-row(no-gutters)
            v-col(cols="12")
              v-list(rounded pa-0 max-width="400px")
                v-list-item-group(color="blue")
                  v-subheader Другие файлы
                  v-list-item(
                    v-for="(file, i) in  otherFiles"
                    :key="i"
                  )
                    v-list-item-content
                      v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                    v-list-item-icon
                      v-btn(
                        outlined
                        fab
                        :href="file.file_path || ''"
                        color="blue"
                        dark
                        class="elevation-0"
                        small
                        target="_blank"
                      )
                        v-icon mdi-download
            v-col(cols="4")
              v-list(rounded pa-0 max-width="400px")
                v-list-item-group(color="blue")
                  v-subheader Акты
                  v-list-item(
                    v-for="(file, i) in  package.pack_files['Акт']"
                    :key="i"
                  )
                    v-list-item-content
                      v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                    v-list-item-icon
                      v-btn(
                        outlined
                        fab
                        :href="file.file_path || ''"
                        color="blue"
                        dark
                        class="elevation-0"
                        small
                        target="_blank"
                      )
                        v-icon mdi-download
            v-col(cols="4")
              v-list(
                rounded
                pa-0
                max-width="400px"
              )
                v-list-item-group(color="blue")
                  v-subheader Счета
                  v-list-item(
                    v-for="(file, i) in package.pack_files['Счет']"
                    :key="i"
                  )
                    v-list-item-content
                      v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                    v-list-item-icon
                      v-btn(
                        outlined
                        fab
                        :href="file.file_path || ''"
                        color="blue"
                        dark
                        class="elevation-0"
                        small
                        target="_blank"
                      )
                        v-icon mdi-download
            v-col(cols="4")
              v-list(rounded pa-0 max-width="600px")
                v-list-item-group(color="blue")
                  v-subheader Счета фактур
                  v-list-item(
                    v-for="(file, i) in  package.pack_files['Счет-фактура']"
                    :key="i"
                  )
                    v-list-item-content
                      v-list-item-title(v-text="file.file_name" :href="file.file_path || ''")
                    v-list-item-icon
                      v-btn(
                        @click.
                        outlined
                        fab
                        :href="file.file_path || ''"
                        color="blue"
                        dark
                        class="elevation-0"
                        small
                        target="_blank"
                      )
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
  data: () => ({
    packageDialogState: false,
    filesDataForUpload: null
  }),
  computed: {
    ...mapState({
      package: state => state.packages.detail,
      packageActiveStatus: state => state.packages.detail.is_active,
      otherFiles: state => state.files.list
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
    }),
    upload () {
      this.$store.dispatch('files/CREATE_FILE', {
        vueFileAgent: this.$refs.vueFileAgent,
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.id,
        filesDataForUpload: this.filesDataForUpload
      })
      this.contragentDialogState = false
      this.filesDataForUpload = null
    },
    fileDeleted (fileData) {
      this.filesDataForUpload = null
    }
  }
}
</script>
