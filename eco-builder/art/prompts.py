"""제미나이(나노 바나나)용 라인 아트 프롬프트 목록 만들기: python3 prompts.py → prompts.md
모든 장에 같은 화풍 문장 + 생물마다 꼭 보여야 할 실제 특징."""
import json, subprocess
STYLE = ("Black ink line art on a pure white background, square 1:1. Scientific field-guide style: realistic anatomy and proportions, "
         "clean confident outlines of even medium weight, fine hatching for texture and shading, no color, no gray fill, no text, "
         "no border, no logo. One subject only, centered, filling about 80% of the frame, slight three-quarter view.")
POWER = " Dramatic, powerful low-angle pose that feels majestic."   # 4줄(최상위 포식자)
F = {  # 생물 → 꼭 보여야 할 특징(영어가 이미지 모델에 더 정확함)
 "해바라기": "a sunflower (Helianthus annuus): large flower head with a spiral seed pattern, ray petals, heart-shaped rough leaves, thick hairy stem",
 "소나무": "a Korean red pine tree (Pinus densiflora): needles in bundles of two, plated bark, small cones, crooked trunk",
 "고사리": "a bracken fern: pinnately divided fronds and a young curled fiddlehead",
 "선인장": "a columnar cactus: ribbed fleshy stem with clusters of spines on areoles, no leaves",
 "부레옥잠": "a water hyacinth floating on water: swollen spongy leaf stalks, glossy round leaves, feathery roots hanging below",
 "검정말": "Hydrilla (an aquatic plant) fully under water: thin stem with whorls of small narrow leaves, water line above",
 "은행나무": "a ginkgo branch in autumn: fan-shaped bilobed leaves, some falling",
 "보리": "barley plants: long awned ears of grain and narrow leaves",
 "자작나무": "a birch tree: white peeling bark with dark horizontal marks, small toothed leaves",
 "버섯": "a group of wild mushrooms growing on a fallen log: caps, gills, stems, mycelium threads in the wood",
 "곰팡이": "bread mold seen under a magnifier: thread-like hyphae and round spore heads on stalks",
 "세균": "soil bacteria under a microscope: rod-shaped and round cells, some with flagella, on soil particles",
 "식물성 플랑크톤": "phytoplankton under a microscope: diatoms with glass-like patterned shells and chain-forming cells",
 "맹그로브": "a mangrove tree on a muddy shore: arching prop roots and pencil-like breathing roots (pneumatophores) sticking up from the mud",
 "연꽃": "a lotus: large round leaf held above water, open flower, lotus root with air channels shown in cross-section",
 "꿀벌": "a honeybee: exactly six legs, two pairs of transparent veined wings, striped hairy abdomen, compound eyes, antennae, pollen basket on hind leg",
 "닭": "a hen: comb and wattles, feathers, scaly legs, pecking grain",
 "양": "a sheep: thick woolly fleece, rectangular pupils, hooves",
 "낙타": "a dromedary camel: single hump, long legs, wide padded feet, long eyelashes",
 "캥거루쥐": "a kangaroo rat: large hind legs for hopping, very long tufted tail, big eyes, holding a seed",
 "달팽이": "a land snail: spiral shell, eye stalks on upper tentacles, muscular foot leaving a trail",
 "다람쥐": "a Siberian chipmunk: five dark stripes on the back, bushy tail, cheek pouches full of acorns",
 "북극토끼": "an Arctic hare in winter: thick white fur, short dark-tipped ears, large furry hind feet in snow",
 "순록": "a reindeer: large branching antlers, thick fur, broad hooves in snow, eating lichen",
 "지렁이": "an earthworm in a soil cross-section: ringed segments, clitellum band, burrow tunnels",
 "쇠똥구리": "a dung beetle: exactly six legs, rolling a ball of dung backward with hind legs",
 "흰개미": "termites: workers with exactly six legs, soft pale bodies, inside wood tunnels",
 "야크": "a yak on a high mountain: very long shaggy hair, curved horns, humped shoulders",
 "올챙이": "tadpoles in water: round body, long tail fin, small external gills visible on one",
 "장구벌레": "mosquito larvae hanging from the water surface by breathing tubes (siphons), segmented bodies, bristles",
 "올빼미": "a tawny owl at night on a branch: large forward-facing eyes, facial disc, hooked beak, sharp talons",
 "박쥐": "a bat flying in a dark cave: membrane wings stretched between long finger bones, large ears, catching a moth",
 "개구리": "a frog sitting on a wet leaf: bulging eyes, smooth moist skin with spots, eardrum (tympanum), webbed hind feet",
 "물총새": "a common kingfisher diving into water: long dagger-like bill, short tail, catching a small fish",
 "사막여우": "a fennec fox in the desert: very large ears, small slender body, thick fur on paws, bushy tail",
 "뱀": "a rat snake coiled: smooth scales, forked tongue, round pupils",
 "두더지": "a mole digging in a soil cross-section: large spade-like front paws with claws, tiny eyes, velvety fur, pointed snout",
 "오소리": "a badger at its burrow entrance: black-and-white striped face, stocky body, long digging claws",
 "잠자리": "a dragonfly: exactly six legs, two pairs of long veined wings held flat, huge compound eyes, long slender abdomen; its aquatic nymph below on a water plant",
 "물방개": "a diving beetle underwater: exactly six legs, flattened oval body, fringed swimming hind legs, an air bubble under the tip of the wings",
 "매": "a peregrine falcon: dark 'mustache' stripe below the eye, hooked beak, pointed long wings spread wide, barred chest, yellow-ringed eye, talons open",
 "물수리": "an osprey grabbing a fish from water: white underside, dark eye stripe, long angled wings, talons gripping the fish",
 "북극곰": "a polar bear on sea ice: massive body, thick fur, long neck, small ears, huge paws",
 "삵": "a leopard cat on a rocky outcrop: spotted coat, two white stripes on the forehead, rounded ears, long tail",
 "범고래": "an orca breaching out of the ocean: tall triangular dorsal fin, white eye patch behind and above the eye, white belly, grey saddle patch behind the fin, tail flukes, splashing water",
 "수달": "a Eurasian otter by a stream: sleek body, small rounded ears, whiskers, webbed paws, long thick tapering tail",
 "산양": "a long-tailed goral on a steep rocky cliff: short backward-curving horns, thick coat",
 "반달가슴곰": "an Asiatic black bear: black fur with a white crescent (V) mark on the chest, round ears",
 "황새": "an Oriental stork in a wetland: white body, black flight feathers, long black bill, red legs",
 "저어새": "a black-faced spoonbill on a tidal flat: spoon-shaped black bill, black bare face, white plumage",
 "장수하늘소": "a Korean longhorn beetle (Callipogon relictus): exactly six legs, very long segmented antennae, large mandibles",
 "원앙": "a male mandarin duck: orange 'sail' feathers on the back, white eye stripe, red bill, on a stream",
 "하늘다람쥐": "a Siberian flying squirrel gliding: fur membrane between front and hind legs, huge dark eyes, flat tail",
}
d = json.loads(subprocess.run(["node", "-e", "import('../game.js').then(m=>console.log(JSON.stringify({c:m.CARDS,n:m.NOBLES})))"], capture_output=True, text=True).stdout)
rows = [(c["id"], c["n"], c["tier"]) for c in d["c"].values()] + [(f"N-{k}", v["n"], 0) for k, v in d["n"].items()]
miss = [n for _, n, _ in rows if n not in F]
assert not miss, f"특징 없는 생물: {miss}"
out = ["# 생태계 짓기 카드 그림 프롬프트 (제미나이 이미지 생성용)", "",
       "- 한 장에 하나씩 생성합니다. 아래 상자 안의 문장을 통째로 붙여 넣으세요.",
       "- 저장할 파일 이름은 '파일' 칸 그대로입니다(예: 1-0.png). 정사각형 이미지로 저장해 주세요.",
       "- 다리 수·무늬 위치 등 특징이 틀리면 다시 생성해 주세요. 올려 주시면 제가 한 장씩 확인합니다.", ""]
for fid, n, tier in rows:
    out += [f"## {n} · 파일 `{fid}.png`", "", "```", f"{F[n]}. {STYLE}{POWER if tier == 4 else ''}", "```", ""]
open("prompts.md", "w", encoding="utf-8").write("\n".join(out))
print(len(rows), "장")
