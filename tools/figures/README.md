# 図版一式 2026-09-13

## 内容

- `figures/` 図版26点。各点 PNG と SVG の両方。重複ファイルなし
- `90_図版対応表.md` 図版対応表。番号、題、形式、出典、ファイル名、廃止した図の履歴
- `figures.py` 図版生成スクリプト。`python3 figures.py` で26点すべてを `figures/` へ再生成する
- `bookstyle.py` / `charts.py` / `chinamodel.py` 上記が使う共通スタイルと作図ヘルパー、中国のコホート要因モデル

## 番号とファイルの対応

| 図 | ファイル |
|---|---|
| 1-1 | fig1-1_energy_per_capita |
| 1-2 | fig1-2_japan_trade |
| 2-1 | fig2-1_computing_price |
| 2-2 | fig2-2_datacenter_demand |
| 2-3 | fig2-3_uk_agriculture |
| 3-1 | fig3-1_us_percapita_break |
| 3-2 | fig3-2_vre_value_system_cost |
| 3-3 | fig3-3_germany_negative_prices |
| 3-4 | fig3-4_research_productivity |
| 4-1 | fig4-1_price_divergence |
| 4-2 | fig4-2_tfr_distribution |
| 4-3 | fig4-3_korea_spend_tfr |
| 4-4 | fig4-4_china_births |
| 4-5 | fig4-5_china_women |
| 4-6 | fig4-6_world_births |
| 5-1 | fig5-1_price_of_light |
| 5-2 | fig5-2_launch_costs |
| 5-3 | fig5-3_solar_learning |
| 5-4 | fig5-4_four_headcounts |
| 6-1 | fig6-1_labour_share |
| 6-2 | fig6-2_wealth_tax |
| 6-3 | fig6-3_citizen_capital |
| 7-1 | fig7-1_unmeasured_economy |
| 7-2 | fig7-2_time_use |
| 8-1 | fig8-1_techno_blocs |
| 8-2 | fig8-2_pentagons |

## この版で直したこと

- 図1-2として二つのファイルが残っていた。日本語版のPDFは、廃止済みの「米国エネルギー支出の対GDP比」を図1-2として組んでいた。日本語版のビルドはファイル名から自動で図番号を拾う作りで、同じ番号のファイルが二つあったため、後に並ぶほうを拾っていた
- 旧番号のまま残っていた `fig1-3_japan_trade` を削除し、`figures.py` の関数名と図中のタイトルを 1-2 に揃えた
- 図5-4だけが `figures.py` の外にあり、再生成の対象から漏れていた。`figures.py` に取り込んだ
