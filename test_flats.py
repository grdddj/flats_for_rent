from pathlib import Path

from get_flats import Flat, get_flat_from_html

HERE = Path(__file__).resolve().parent

FLAT_HTML = """\
<div class="w-layout-grid seznam-bytu-grid"><div class="name-enttry-title" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef300-59f36908">QA-01-01</div><div class="table-entty-wrapper" id="w-node-_3163eacc-0e30-b592-19ae-ba7cf1134f15-59f36908"><div class="table_title-tablet">budova</div><div fs-cmsfilter-field="budova" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef302-59f36908">A</div></div><div class="table-entty-wrapper" id="w-node-_26d1d1f2-f38a-f99f-4edc-173e9b4520c1-59f36908"><div class="table_title-tablet">podlaží</div><div fs-cmsfilter-field="podlazi" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef304-59f36908">1.NP</div></div><div class="table-entty-wrapper" id="w-node-_9ebcc4bc-75bb-0804-7540-824c56aa43df-59f36908"><div class="table_title-tablet">dispozice</div><div fs-cmsfilter-field="dispozice" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef306-59f36908">1+kk</div></div><div class="table-entty-wrapper" id="w-node-_064036f0-39ad-2de1-f512-bd94d7d4c52e-59f36908"><div class="table_title-tablet">plocha (m<sup>2</sup>)</div><div fs-cmsfilter-field="plocha" fs-cmssort-field="plocha" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef308-59f36908">28.2</div></div><div class="table-entty-wrapper" id="w-node-_096f7b4b-a322-d334-9220-b818e137a4f9-59f36908"><div class="table_title-tablet">terasa/balkón<br/>/předzahrádka (m<sup>2</sup>)</div><div fs-cmsfilter-field="plocha" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef30a-59f36908">14.0</div></div><div class="table-entty-wrapper" id="w-node-_11ef289b-1527-ce4f-fb51-312ccd98dda3-59f36908"><div class="table_title-tablet">vybavený</div><div class="flex-horizontal" id="w-node-_77b55ba9-e36a-0eb7-fd5c-fb14344e4af8-59f36908"><div class="hidden-text-filter" fs-cmsfilter-field="vybavenost" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef30d-59f36908">ANO</div><div>ANO</div><div class="w-condition-invisible">NE</div></div></div><div class="table-entty-wrapper" id="w-node-_10c6cc41-88a4-eb97-63f9-37f92ded8d44-59f36908"><div class="table_title-tablet">cena</div><div class="flex-horizontal" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef311-59f36908"><div class="flex-horizontal"><div fs-cmsfilter-field="cena" fs-cmssort-field="cena">24 000</div><div> Kč</div><div class="w-dyn-bind-empty"></div><div class="w-condition-invisible"> €</div></div><div class="flex-horizontal w-condition-invisible"><div class="w-dyn-bind-empty"></div><div class="w-condition-invisible"> €</div></div></div></div><div class="flex-horizontal top-pad-mob-list" id="w-node-_9e50e461-e499-3e8c-40aa-39f3537ef31a-59f36908"><a class="list-button cz w-inline-block" href="https://cdn.prod.website-files.com/65e70bb1c2b49bacc10a5340/660ed762b9022602ddea20ad_HAG_karta_atelieru_QA-01-01.pdf" target="_blank"><div>detail</div></a><a class="list-button en w-inline-block" href="https://cdn.prod.website-files.com/65e70bb1c2b49bacc10a5340/662f75a168c4cc3400e42b96_HAG_atelier_card_QA-01-01.pdf" target="_blank"><div>detail</div></a><div class="horizontal-spacer"></div><a byt="QA-01-01" class="bttn_poptat outlined w-inline-block" data-w-id="d39fdbbe-28f5-3ea4-f03c-df236a0f87f4" href="#"><div>poptat</div></a></div><div class="table-entty-wrapper" id="w-node-a20b2b6d-ac5e-7638-d135-3f39acc7877c-59f36908"><div class="table_title-tablet">stav</div><div class="flex-horizontal" id="w-node-_129158d7-b635-6e36-d204-f99d1a347038-59f36908"><div class="dostupnost diff w-condition-invisible"><div class="stav-text" fs-cmsfilter-field="stav">Volný od </div><div class="dostupnost abs w-condition-invisible"></div></div><div class="flex-horizontal"><div class="stav-text" fs-cmsfilter-field="stav">Volný od </div><div class="stav-text">1.1.2025</div></div><div class="dostupnost rez w-condition-invisible"><div class="stav-text" fs-cmsfilter-field="stav">Volný od </div></div></div></div></div>
"""


def test_get_flat_from_html():
    flat = get_flat_from_html(FLAT_HTML)
    assert isinstance(flat, Flat)
    assert flat.id == "QA-01-01"
    assert flat.building == "A"
    assert flat.floor == 1
    assert flat.disposition == "1+kk"
    assert flat.price == 24000
    assert flat.size == 28.2
    assert flat.balcony_size == 14.0
    assert flat.furnished == True
    assert flat.reserved == False
