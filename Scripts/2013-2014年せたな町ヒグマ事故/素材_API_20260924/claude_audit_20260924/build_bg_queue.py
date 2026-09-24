#!/usr/bin/env python3
"""背景（16:9・人物なし）の再生成キューを作る。ChatGPTのブラウザ生成（run.py）用。
id は納品ファイル名と一致させる（ASSET-NNN_still / ASSET-NNN_bg）。
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
plan = json.load(open(HERE / "repair_plan.json"))
inv = json.load(open(HERE / "inventory.json"))
spec = {a["asset"]: a for a in json.load(open(HERE / "spec.json"))}

HEAD = ("Generate one photorealistic image, 16:9 landscape. A documentary background plate (a cartoon character will be overlaid later on the left). "
        "Setting: Setana and Imakane area, southwestern Hokkaido, Japan. ")
TAIL = (" Natural light, restrained Japanese documentary photography, realistic materials and terrain, shot on RED camera, "
        "wide 16:9 landscape composition, the left third kept as calm open space. Crucial: this is an EMPTY BACKGROUND PLATE. "
        "No people, no hands, no arms, no body parts, no human silhouettes, no reflections of people, no vehicles with drivers. "
        "No readable text, no lettering, no signage wording, no logo, no emblem, no collage, no split screen unless stated, no cartoon art. "
        "Generate one image only.")
SPRING = "Early spring in mid April, bare deciduous trees, brown grass, small patches of old snow only in shade. "
BEAR = ("The bear is an adult male Hokkaido brown bear, species-scale body about 2 metres long, dark brown coat, ON ALL FOURS, "
        "NOT standing upright, NOT on two legs. ")
FEROCIOUS = ("Its jaws are wrenched wide open in a savage snarl with the teeth bared, ears pinned flat against the skull, "
             "the fur along its neck and shoulders bristled up into a raised ridge, head dropped low between bunched shoulders, "
             "claws hooked into the soil. Ferocious, enraged, single-minded predatory fury. ")
DIM = "Dim but NOT pure black; every main element stays clearly readable. "
NIGHT = "At night, lit only by a porch lamp and a distant streetlight. " + DIM

S = {
"ASSET-004": SPRING + "Close-up of an abandoned woman's olive-green field jacket lying crumpled on the forest floor among dead leaves and dry grass, one sleeve twisted, damp soil, a few bare twigs across it. Nothing else in frame.",
"ASSET-014": "Aerial view from high above the Sea of Japan coast: a rugged wooded shoreline of southwestern Hokkaido, grey-blue sea on the left, brown early-spring coastal forest and low hills on the right, a small town of low roofs tucked in a bay. " + SPRING,
"ASSET-015": SPRING + "A small white Japanese station wagon seen from directly behind, driving away up a narrow gravel forest road that curves into bare woodland on a hillside; the rear of the car and the road ahead are the subject. Camera at road level about ten metres behind. No driver visible through the rear window.",
"ASSET-020": SPRING + "A small white Japanese station wagon parked on a gravel track beside a shallow mountain stream, rear hatch closed, doors closed, no one around; bare trees and dry grass, a few patches of old snow on the bank.",
"ASSET-022": SPRING + "A narrow muddy mountain path through bare deciduous woodland near a stream, seen from adult eye height about four metres back; the path runs from the lower right into the trees; grey overcast daylight. Empty path.",
"ASSET-023": SPRING + "Dense mountain woodland with a faint trail through leaf litter and low bamboo grass beside a small stream, seen from eye height; the trail leads away between thin bare trunks. Empty woodland.",
"ASSET-025": SPRING + "A small mountain stream in a shallow wooded gully, seen from a distance from slightly above, stones and dry grass along the bank, bare trees; at the far bank near the water a grey blanket-shaped form lies covered on the ground, too far to see any detail, no body parts visible.",
"ASSET-026": SPRING + "The bank of a small mountain stream at eye height: on the wet stones near the water a grey wool blanket is laid over a low shape on the ground, fully covered, nothing of what is under it visible; bare trees and dry grass behind. No one present.",
"ASSET-028": SPRING + "In the foreground on a flat rock a plain clipboard with a blank form and a pencil; in the far background, out of focus, a blue tarp laid flat over a low shape on the forest floor with nothing showing. Wide composition, no people.",
"ASSET-031": "Interior of a modest Japanese farmhouse living room: a low wooden table with an open plain pocket diary (blank pages, no writing) and, next to it, a small framed family photograph placed face down; soft window light. No people.",
"ASSET-032": "Interior of a small rural town office: a wooden desk with an open plain ledger showing empty ruled columns, a pen laid across it, a black desk telephone beside; morning window light. No writing, no people.",
"ASSET-033": SPRING + "A steep wooded hillside with patches of old snow, thin bare trees and low bamboo grass, seen from below looking up the slope; open ground between the trunks where searchers could spread out. Empty slope.",
"ASSET-036": "Interior of a town office: on a desk a neat stack of plain white official documents and five brown envelopes, a rubber stamp and an ink pad beside them; grey window light. No writing visible, no people.",
"ASSET-038": SPRING + "A grey van parked at the edge of a gravel forest road at a trailhead, side door closed, bare trees and a wooded slope behind, a small stream sign-less path entering the woods. No people.",
"ASSET-039": "Interior of a small rural town office meeting room: a plain table with three empty chairs, a few closed folders and a pot of tea on the table, a whiteboard with nothing written, window light. No people.",
"ASSET-041": SPRING + "Close-up on the forest floor: a small tuft of dark brown bear hair caught on dead leaves and a twig, next to it an open empty clear plastic specimen tube with a white cap and a pair of tweezers laid on the leaves. No hands.",
"ASSET-043": "Pre-dawn in early spring in mid April: a narrow forest road entering dark bare woodland, faint blue light on the horizon, patches of old snow beside the track glowing faintly, mist between the trunks. " + DIM + " Empty road.",
"ASSET-044": SPRING + "A dense thicket of chest-high sasa bamboo grass under bare trees on a hillside, seen from eye height; leaves overlapping, no path, no one visible. Empty thicket.",
"ASSET-045": SPRING + "A rural paved road with a wooden warning signboard on a post at the roadside showing only a black bear pictogram and no wording, bare trees and fields beyond, grey sky. No people, no cars.",
"ASSET-049": SPRING + "Three steel mesh box traps for bears placed among bare trees in a mountain forest, doors open, a little bait inside, leaf litter and old snow around. No people.",
"ASSET-051": SPRING + "A weathered wooden community notice board on posts beside a village road, a blank sheet of white paper pinned to it, low houses and bare trees behind. No wording, no people.",
"ASSET-053": SPRING + "The side of a rural Japanese farmhouse where a dense wall of tall sasa bamboo grass grows right up to the wooden fence, a sickle and a rake leaning against the fence, wooded hillside behind. No people.",
"ASSET-054": SPRING + "A small white Japanese school microbus with a rounded front parked at the gate of a rural farmhouse, door closed, no one inside, gravel drive, wooded hills behind, morning light. No lettering on the bus.",
"ASSET-055": "Interior of a rural town office reception counter: a black push-button desk telephone and a blank report form with a pen on the counter, a low shelf of binders behind, window light. No writing, no people.",
"ASSET-058": SPRING + "The open rear hatch of a grey van at a forest road; laid out on a folding table beside it are hunting gear items: a blaze-orange vest, a cap, binoculars, a folded map, a thermos and a closed gun case. No people.",
"ASSET-059": "Interior close-up on a wooden desk: a blank application form with a pen and a rubber stamp, and next to it a closed dark hard gun case with a padlock; soft window light. No writing, no people.",
"ASSET-060": SPRING + "An empty steel mesh box trap for bears standing on the forest floor among bare trees, door raised open, nothing inside, dead leaves and thin old snow around it. No people.",
"ASSET-064": SPRING + "A narrow gravel mountain road through mixed forest near Ota, southwestern Hokkaido, curving away between bare trees and a few conifers, low hills beyond, overcast light. Empty road, no vehicles.",
"ASSET-066": SPRING + "A narrow forest trail climbing gently into bare woodland with young green sprouts of wild garlic along the edges, morning light between the trunks. Empty trail.",
"ASSET-067": SPRING + "Close-up on the forest floor of two woven bamboo baskets side by side filled with freshly picked wild garlic leaves (gyoja ninniku), dead leaves around them. No hands.",
"ASSET-068": "A simple kitchen scale on a rough wooden table with a bundle of wild garlic leaves lying on the pan, soft daylight from a window, a folded newspaper without readable print beside it. No hands, no people.",
"ASSET-069": SPRING + "A forest trail entrance at the edge of a gravel road, a small worn path leading up between bare trees and bamboo grass, morning light; two empty woven baskets left at the trailhead. No people.",
"ASSET-071": SPRING + "A forest road entrance with a plain wooden signboard on posts (blank, no wording) beside the path where it enters the woods; bare trees, bamboo grass, thin old snow. No people.",
"ASSET-074": SPRING + "A forest path descending a slope, seen from the side, with a view between the trees down to the grey Sea of Japan in the distance; bare trunks, dry grass. Empty path.",
"ASSET-075": SPRING + "Side view of a narrow mountain path through bare trees. " + BEAR + FEROCIOUS + "It is charging along the path from the right edge toward the left in full profile, mid-stride, so its whole length is visible across the frame; the left third of the frame is empty path where a person overlay will be placed. No people.",
"ASSET-076": SPRING + "Side view of a narrow mountain path through bare trees. " + BEAR + FEROCIOUS + "It is lunging low from the right toward the left with its front paws leaving the ground, in full profile, the moment before contact; the left third of the frame is left empty for a person overlay. No people.",
"ASSET-078": SPRING + "Close-up of a Japanese nata hatchet (short heavy blade with a wooden handle) lying on the ground on dead leaves and moss beside a forest path, a few cut twigs next to it. No hands.",
"ASSET-079": SPRING + "A narrow forest road between bare trees and bamboo grass. " + BEAR + "It stands on the road about fifteen metres away facing the camera, head low, ears back, mouth slightly open and menacing; the left third of the frame is empty road for a person overlay to show scale. No people, no vehicles.",
"ASSET-081": SPRING + "A narrow mountain path through bare trees. " + BEAR + "It is recoiling: head jerked to one side, front legs braced backward, body twisted as it staggers back along the path, mouth open, eyes narrowed, clearly hurt and thrown off balance but with no visible wound. No people.",
"ASSET-084": "Interior of a quiet hospital corridor: pale walls, a row of empty waiting chairs, a folded grey blanket on one chair, morning light from a window at the end, no signage wording, no real institution name or emblem. No people.",
"ASSET-088": SPRING + "An old rural Japanese wooden school building with a grey roof seen across a dry schoolyard, and directly behind it a wooded mountain rising close, bare trees with patches of old snow. No people, no readable signs.",
"ASSET-090": SPRING + "A mountain road shoulder with two new yellow warning signs on a metal post showing only a bear pictogram and no wording, gravel, bamboo grass and bare trees behind. No people.",
"ASSET-091": SPRING + "The back garden of a rural farmhouse: a vegetable plot, a low fence, and right behind it a steep wooded hill of bare trees and bamboo grass, overcast light. No people.",
"ASSET-092": SPRING + "Close-up on a wooden bench at the edge of a field: a metal whistle on a red cord and a small bundle of firecrackers with a lighter, a pair of work gloves beside them. No hands.",
"ASSET-101": SPRING + "Two hiking backpacks placed on a fallen log beside a forest trail, each with a brass bear bell hanging from a strap, dead leaves and bamboo grass around. No people.",
"ASSET-102": SPRING + "A narrow winding footpath through bare woodland with green sprouts along the edges, soft morning light through the branches. Empty path.",
"ASSET-103": SPRING + "A narrow mountain path with a woven bamboo basket knocked over on its side, wild garlic leaves spilled onto the ground, dead leaves scattered, thin trees around. No people.",
"ASSET-104": "Interior of a research office: a wooden desk with three closed plain case folders in a row, a magnifying glass and a pencil, a bookshelf out of focus behind; soft window light. No writing, no people.",
"ASSET-107": SPRING + "A wide view from a hilltop across several forested ridges receding into the distance, bare grey-brown woodland with snow patches on the shaded slopes, low cloud, southwestern Hokkaido. No people.",
"ASSET-108": SPRING + "A dense sasa bamboo thicket at the edge of bare woodland. " + BEAR + "It is walking away from the camera into the thicket, only its back, rump and hind legs visible, its head already hidden in the leaves; calm retreat, no snarl. No people.",
"ASSET-110": "Interior of a town office desk by a window: a blank official request form with a pen and a stamp on the desk; through the window, a red-and-white rescue helicopter parked on a helipad in the distance, no markings or lettering. No people.",
"ASSET-111": SPRING + "A wide view of forested mountains with a small helicopter flying high above the ridge in an overcast sky, seen from a clearing at the forest edge; bare trees, old snow patches. No people.",
"ASSET-113": SPRING + "A gravel forest road where several vehicles are parked in a row along the edge: two grey vans and a small red fire-brigade truck without lettering, bare trees behind. No people.",
"ASSET-115": SPRING + "A junction where a forest path splits into three narrower trails going off in different directions between bare trees and bamboo grass, seen from eye height. Empty trails.",
"ASSET-117": SPRING + "Close-up of a bolt-action hunting rifle laid on the hood of a grey van beside a forest road, a small cleaning kit next to it, bare trees behind. No hands.",
"ASSET-118": SPRING + "A steep wooded slope with old snow, seen from partway up, and far above the ridge a small helicopter in a grey sky; bare trees, bamboo grass. No people.",
"ASSET-119": SPRING + "A shaded hollow in a bare forest where old spring snow still lies in a dirty white patch between the roots, meltwater trickling, dead leaves on the surface. No people.",
"ASSET-120": SPRING + "Close-up of a large bear paw print pressed into wet old snow on a mountain path, claw marks visible, more prints leading away, bare trees around. No people.",
"ASSET-122": SPRING + "A line of large bear paw prints across a patch of wet spring snow on a forest path, seen from eye height going away from the camera, bare trees. No people.",
"ASSET-125": SPRING + "A wide empty mountain landscape of bare forested ridges under a grey sky, and far off a small helicopter flying away toward the horizon; no bear, no people.",
"ASSET-128": NIGHT + "A small rural village at night: the closed wooden front door of a farmhouse with a glowing porch lamp, a few low houses along a dark lane, the black outline of a wooded hill behind. No people.",
"ASSET-136": "Interior of a laboratory bench: a sealed clear specimen bag with a small dark tissue sample, a white insulated shipping box open beside it with an ice pack, a blank label. No hands, no people.",
"ASSET-137": SPRING + "A steel mesh box trap for bears set among bare trees on a wooded hillside near a stream, door open, leaf litter and old snow. No people.",
"ASSET-140": "Interior close-up: a single plain brown envelope lying unopened on a wooden desk by a window, a letter opener beside it, soft daylight. No hands, no people.",
"ASSET-141": "Interior close-up: two plain brown envelopes lying side by side on a dark laboratory table with a clear gap between them, nothing written on them, cool light. No hands.",
"ASSET-142": "Interior of a town office: on a desk two open cardboard filing boxes side by side and a single blank index card lying between them, a pen; window light. No writing, no people.",
"ASSET-145": "Interior of a town meeting room: a long table with several printed photographs of a brown bear and a map laid out (no readable print), a whiteboard with nothing written, chairs pushed in. No people.",
"ASSET-146": "Interior of a task-force office: a desk piled with stacks of plain paper reports and a large folded map, a black telephone and a mug; window light. No writing visible, no people.",
"ASSET-148": "Interior of a town hall meeting room seen from the podium: a microphone on a wooden lectern in the foreground, rows of empty chairs, a plain banner with no wording, daylight through tall windows. No people.",
"ASSET-149": SPRING + "A wooden notice board on posts at the entrance of a mountain path, a blank white notice pinned on it, the path behind roped off with a plain rope, bare trees. No wording, no people.",
"ASSET-151": "Interior close-up on a wooden desk: a plain blank search plan document in a folder, a printed photograph of a snowy mountain forest, a pair of gloves, soft window light. No writing, no hands.",
"ASSET-152": "Two plain wall calendars hung side by side on a beige office wall, each showing a month grid with a mountain landscape photo above, no readable numbers or text. No people.",
"ASSET-157": "Interior of a rural town office: a window framing a view of a quiet village street with low houses, a wooded hill behind, a desk with a folder in the foreground. No people inside or outside.",
"ASSET-158": SPRING + "A snowy ridge path through bare trees with a line of large bear paw prints leading away along it, low cloud. No people.",
"ASSET-160": SPRING + "An unused steel mesh box trap for bears placed at the edge of a mountain road, door raised open, no bait, gravel and bamboo grass. No people.",
"ASSET-162": SPRING + "A distant view across a clearing: " + BEAR + "It is far away at the forest edge, seen in profile, small in the frame, calm, its snout turned slightly toward the camera, no visible injury, no snarl. No people.",
"ASSET-166": SPRING + "A row of four ordinary Japanese cars parked on the shoulder of a narrow mountain road beside bare woods, no one around, doors closed. No people.",
"ASSET-167": "Interior close-up on an office desk: printed photographs of a brown bear and a map laid out, a walkie-talkie and a clipboard with a blank form beside them, a pen. No hands, no people.",
"ASSET-168": SPRING + "An abandoned overgrown field of dry brown weeds bordered by a dark line of bare forest at the foot of a hill, a leaning fence post, overcast light. No people.",
"ASSET-169": "A rough wooden shelf in a field shed: a small portable radio with its antenna up and a metal whistle on a cord lying beside it, a coil of rope, daylight from the open door. No hands.",
"ASSET-170": SPRING + "A small rural village of low houses with dark roofs at the foot of a steep wooded hill, seen from the edge of a field, shutters closed, morning light. No people.",
"ASSET-172": SPRING + "A wide view over a broad expanse of bare deciduous forest filling the hills between two districts of southwestern Hokkaido, patches of snow on the slopes, low cloud. No people.",
"ASSET-174": SPRING + "A forest trail entering dark woodland from a gravel road, a wooden post at the entrance without wording, bare trees and bamboo grass. Empty trail.",
"ASSET-175": SPRING + "A high wide view over a very broad forested valley and ridges in bare early-spring colour, far larger than a single hill, snow in the shaded folds, overcast sky. No people.",
"ASSET-178": "Interior of a small Japanese convenience store counter: a neat stack of printed flyers showing a bear photograph placed on the counter beside a tray, shelves out of focus behind, no readable text. No people.",
"ASSET-179": "Close-up of a single blank white flyer sheet pinned flat on a wooden notice board, slightly creased, soft daylight, nothing printed on it. No hands.",
"ASSET-181": "Interior: a split composition on one laboratory table, left half a folded map with a blank search log and a compass, right half a rack of clear DNA sample tubes with blank labels; cool daylight. No people.",
"ASSET-184": "Interior of a laboratory: a white rack holding twenty clear sample tubes with white caps, each with a small blank label, on a black bench by a window. No hands, no people.",
"ASSET-187": "Interior close-up: twenty plain brown envelopes laid out in four rows of five on a dark laboratory table, all identical and blank; cool light. No hands.",
"ASSET-188": "Summer in early August: a wide field of green sugar-beet leaves in Imakane, southwestern Hokkaido, bordered by a dark green forest and low wooded hills under a bright cloudy sky. No people.",
"ASSET-191": "Summer in early August: a steel mesh box trap for bears set at the edge of a green sugar-beet field, door open, empty inside, forest and hills behind. No people, no bear.",
"ASSET-194": SPRING + "A view from a wooded ridge in Setana over bare hills descending to the grey Sea of Japan, the coastline visible on the left, low cloud. No people.",
"ASSET-196": "A split composition with a thin black line down the middle: left half, early spring in mid April, a green coastal headland above the grey Sea of Japan; right half, midsummer in August, a wide green sugar-beet field with forested hills behind. No people on either side.",
"ASSET-197": "Interior close-up: a single sealed plain brown envelope lying on a polished meeting table, a wooden name plate without lettering beside it, window light. No hands, no people.",
"ASSET-199": "Interior close-up of an office desk: a cup of green tea, a closed folder and a pair of reading glasses laid down, window light on the wood. No hands, no people.",
"ASSET-200": SPRING + "The inside of an open outdoor storage cabinet at a rural house: a plastic box with a whistle, firecrackers, a flashlight and a small radio being put away on the shelf, gravel yard and low house behind. No people.",
"ASSET-202": SPRING + "On the forest floor a plain case file folder lies open on a flat rock in the foreground, and in the background an empty steel box trap among bare trees. No hands, no writing.",
"ASSET-203": SPRING + "A snowy mountain path through bare trees, and on a rock at the path edge a plain document folder with a printed photograph of woodland, no readable text. No hands.",
"ASSET-204": "Summer in early August: a steel mesh box trap for bears set at the edge of a green sugar-beet field, empty, and in the foreground on a wooden crate a plain capture record clipboard with a pen. No people, no bear, no writing.",
"ASSET-206": SPRING + "Close-up on mossy forest ground: a Japanese nata hatchet with a wooden handle and, beside it, a clear specimen tube with a white cap lying on the leaves. No hands.",
"ASSET-207": "Close-up on a weathered wooden picnic table outdoors: two plain brown envelopes side by side and a plain cardboard archive box behind them, a view of hills and sea beyond. No hands.",
"ASSET-210": SPRING + "Close-up on a canvas cloth laid on a rock beside a mountain path: a brass bear bell, a metal whistle and a small closed notebook arranged in a row, old snow at the edge. No hands.",
"ASSET-211": SPRING + "Close-up of a mountain path: a large bear paw print in the mud and, right beside it, a brass bell and a small portable radio lying on the dry grass. No people.",
"ASSET-213": SPRING + "A ridge path through low bamboo grass with a wide view down to the grey sea and snowy hills, overcast light. Empty path.",
"ASSET-214": SPRING + "A forest road climbing gently between bare trees and a wall of bamboo grass on the right, snowy mountain visible ahead. Empty road.",
"ASSET-215": SPRING + "A folding table at a gravel trailhead car park with hiking gear laid out: two backpacks, trekking poles, a gas canister, a first-aid pouch and a bear bell; a car and bare trees behind. No people.",
"ASSET-218": SPRING + "A wooden information board at a trailhead with a map panel and a bear pictogram notice (no readable text), and a small wooden box holding a red bear-spray canister, roped path behind, old snow. No people.",
}

missing = [a for a in plan["bg_regen"] if a not in S]
extra = [a for a in S if a not in plan["bg_regen"]]
assert not missing, f"prompts missing for {missing}"
assert not extra, f"extra prompts {extra}"
queue = []
for a in plan["bg_regen"]:
    files = inv[a]; key = "still" if "still" in files else "bg"
    queue.append({"id": f"{a}_{key}", "asset_no": int(a.split("-")[1]), "kind": spec[a]["category"], "slot": key, "aspect": "16:9",
                  "label": "", "narration": spec[a]["narration"], "char_ref": None, "body": S[a], "prompt": HEAD + S[a] + TAIL})
work = HERE / "regen_bg"; work.mkdir(exist_ok=True)
(work / "image_queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=2))
print("queue:", len(queue), "→", work / "image_queue.json")
