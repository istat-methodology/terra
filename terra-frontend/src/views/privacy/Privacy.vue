<template>
  <div class="row" role="heading" aria-level="1">
    <div class="col-sm-12 col-md-12" title="Privacy">
      <div class="card p-4">
        <div class="card-body p-4">
          <div class="p-4">
            <p style="line-height: normal">
              <b
                ><span style="font-size: 24pt">{{
                  $t("privacy.title_1")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt"
                >{{ $t("privacy.paragraph_1") }}
              </span>
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_2")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_2a")
              }}</span
              ><a href="mailto:protocollo@postacert.istat.it"
                ><span style="font-size: 12pt; color: blue"
                  >protocollo@postacert.istat.it</span
                ></a
              ><span style="font-size: 12pt"
                >;{{ $t("privacy.paragraph_2b") }} : +39 06.46731).</span
              >
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_3")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt"
                >{{ $t("privacy.paragraph_3") }} </span
              ><a href="mailto:responsabileprotezionedati@istat.it"
                ><span style="font-size: 12pt; color: blue"
                  >responsabileprotezionedati@istat.it</span
                ></a
              ><span style="font-size: 12pt">.</span>
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_4")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_4")
              }}</span>
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_5")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_5a")
              }}</span>
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_5b")
              }}</span>
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_5c")
              }}</span>
            </p>

            <!--ul type="disc">
              <li style="line-height: normal">
                <span style="font-size: 12pt">{{
                  $t("privacy.paragraph_5d")
                }}</span>
              </li>
              <li style="line-height: normal">
                <span style="font-size: 12pt">{{
                  $t("privacy.paragraph_5e")
                }}</span>
              </li>
            </ul-->

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_5f")
              }}</span>
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 12pt">{{
                  $t("privacy.paragraph_5g")
                }}</span></b
              ><span style="font-size: 12pt"
                ><br />
                {{ $t("privacy.paragraph_5h") }}
              </span>
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">
                {{ $t("privacy.paragraph_5i") }}</span
              >
            </p>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_6")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_6a")
              }}</span>
            </p>

            <ul type="disc">
              <li style="line-height: normal">
                <span style="font-size: 12pt">{{
                  $t("privacy.paragraph_6b")
                }}</span>
              </li>
              <li style="line-height: normal">
                <span style="font-size: 12pt">{{
                  $t("privacy.paragraph_6c")
                }}</span
                ><a href="mailto:responsabileprotezionedati@istat.it"
                  ><span style="font-size: 12pt; color: blue"
                    >responsabileprotezionedati@istat.it</span
                  ></a
                >
              </li>
            </ul>

            <p style="line-height: normal">
              <b
                ><span style="font-size: 18pt">{{
                  $t("privacy.title_7")
                }}</span></b
              >
            </p>

            <p style="line-height: normal">
              <span style="font-size: 12pt">{{
                $t("privacy.paragraph_7")
              }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Context } from "@/common"
export default {
  name: "Privacy",
  created() {
    this.$store.dispatch("coreui/setContext", Context.Privacy)
  }
}
</script>

<style scoped>
.material-design-icon > .material-design-icon__svg {
  bottom: -0.17rem;
}
.card-body {
  padding-bottom: 0.5rem;
}
a {
  text-decoration: underline;
}
a:not([href]) {
  background-color: transparent;
  color: #321fdb;
}
a:not([href]):hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
