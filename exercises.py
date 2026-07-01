#!/usr/bin/env python3
"""Curated geriatric home exercise library (bilingual EN/CN).

26 evidence-based, senior-safe exercises across five categories. Each entry
includes target muscles, concise instructions, dosage, progression,
regression, and a safety cue -- designed for printed clinical use.
"""

# Each category: (key, {'en': ..., 'cn': ...}, [exercises])
# Each exercise: dict with bilingual fields for name, target, setup, action,
#   dose (language-neutral), progress, regress, safety.

EXERCISE_CATEGORIES = [

    # ── Lower-limb strength ──
    ('strength_lower', {
        'en': 'Resistance \u2014 Lower Limb',
        'cn': '\u6297\u963b\u8bad\u7ec3\uff08\u4e0b\u80a2\uff09',
    }, [
        {
            'name': {'en': 'Sit-to-Stand', 'cn': '\u5750\u7ad9'},
            'target': {'en': 'Quadriceps, glutes', 'cn': '\u80a1\u56db\u5934\u808c\u3001\u81c0\u808c'},
            'setup': {'en': 'Seated in a sturdy chair, feet shoulder-width.', 'cn': '\u5750\u4e8e\u7a33\u56fa\u6905\u5b50\uff0c\u53cc\u811a\u4e0e\u80a9\u540c\u5bbd\u3002'},
            'action': {'en': 'Lean forward, stand fully, sit slowly.', 'cn': '\u8eab\u4f53\u524d\u503e\uff0c\u5b8c\u5168\u7ad9\u8d77\uff0c\u518d\u7f13\u6162\u5750\u4e0b\u3002'},
            'dose': '10\u201315 \u00d7 2\u20133',
            'progress': {'en': 'Hold light dumbbell', 'cn': '\u624b\u6301\u8f7b\u54d1\u94c3'},
            'regress': {'en': 'Use armrests', 'cn': '\u6276\u624b\u628a\u501f\u529b'},
            'safety': {'en': 'Chair against wall', 'cn': '\u6905\u5b50\u9760\u5899'},
        },
        {
            'name': {'en': 'Glute Bridge', 'cn': '\u81c0\u6865'},
            'target': {'en': 'Glutes, hamstrings', 'cn': '\u81c0\u808c\u3001\u8158\u7ef3\u808c'},
            'setup': {'en': 'Supine, knees bent, feet flat.', 'cn': '\u4ef0\u5367\uff0c\u5c48\u819d\uff0c\u53cc\u811a\u8e2a\u5730\u3002'},
            'action': {'en': 'Squeeze glutes, lift hips, lower slowly.', 'cn': '\u6536\u7d27\u81c0\u808c\uff0c\u62ac\u9ad8\u9ac4\u90e8\uff0c\u7f13\u6162\u4e0b\u843d\u3002'},
            'dose': '10 \u00d7 2',
            'progress': {'en': 'Single-leg bridge', 'cn': '\u5355\u817f\u81c0\u6865'},
            'regress': {'en': 'Smaller range', 'cn': '\u51cf\u5c0f\u5e45\u5ea6'},
            'safety': {'en': 'No lower-back arch', 'cn': '\u8170\u90e8\u52ff\u8fc7\u4f38'},
        },
        {
            'name': {'en': 'Side-lying Hip Abduction', 'cn': '\u4fa7\u5367\u9acb\u5916\u5c55'},
            'target': {'en': 'Gluteus medius', 'cn': '\u81c0\u4e2d\u808c'},
            'setup': {'en': 'Side-lying, bottom knee bent.', 'cn': '\u4fa7\u5367\uff0c\u4e0b\u65b9\u819d\u5c48\u66f2\u3002'},
            'action': {'en': 'Lift top leg to 30\u201345\u00b0, lower slowly.', 'cn': '\u62ac\u9ad8\u4e0a\u65b9\u817f\u81f3 30\u201345\u00b0\uff0c\u7f13\u6162\u4e0b\u843d\u3002'},
            'dose': '10\u201312 / side \u00d7 2',
            'progress': {'en': 'Ankle weight', 'cn': '\u811a\u8155\u6c99\u888b'},
            'regress': {'en': 'Smaller range', 'cn': '\u51cf\u5c0f\u5e45\u5ea6'},
            'safety': {'en': 'No hip roll-back', 'cn': '\u8eab\u4f53\u52ff\u540e\u4ef0'},
        },
        {
            'name': {'en': 'Standing Calf Raise', 'cn': '\u7ad9\u7acb\u63d0\u8e35'},
            'target': {'en': 'Gastrocnemius, soleus', 'cn': '\u8153\u80a0\u808c\u3001\u6bd4\u76ee\u9c7c\u808c'},
            'setup': {'en': 'Stand behind chair, light fingertip support.', 'cn': '\u7ad9\u4e8e\u6905\u80cc\u540e\uff0c\u624b\u6307\u8f7b\u6276\u3002'},
            'action': {'en': 'Rise onto toes, hold 2 s, lower.', 'cn': '\u8e35\u8db3\u62ac\u8d77\uff0c\u4fdd\u6301 2 \u79d2\uff0c\u4e0b\u843d\u3002'},
            'dose': '10\u201315 \u00d7 2',
            'progress': {'en': 'Single leg', 'cn': '\u5355\u817f'},
            'regress': {'en': 'Seated calf raise', 'cn': '\u5750\u4f4d\u63d0\u8e35'},
            'safety': {'en': 'Lower slowly (eccentric)', 'cn': '\u7f13\u6162\u4e0b\u843d\uff08\u79bb\u5fc3\uff09'},
        },
        {
            'name': {'en': 'Wall Sit', 'cn': '\u9760\u5899\u9759\u8e94'},
            'target': {'en': 'Quadriceps', 'cn': '\u80a1\u56db\u5934\u808c'},
            'setup': {'en': 'Back against wall, feet 30 cm out.', 'cn': '\u80cc\u9760\u5899\uff0c\u53cc\u811a\u524d\u79fb 30 cm\u3002'},
            'action': {'en': 'Slide down to semi-squat, hold, stand up.', 'cn': '\u4e0b\u6ed1\u81f3\u534a\u8e72\uff0c\u4fdd\u6301\uff0c\u7ad9\u8d77\u3002'},
            'dose': 'Hold 10\u201330 s \u00d7 3',
            'progress': {'en': 'Deeper squat', 'cn': '\u66f4\u6df1\u8e72\u4f4d'},
            'regress': {'en': 'Shallower angle', 'cn': '\u66f4\u6d45\u89d2\u5ea6'},
            'safety': {'en': 'Knees behind toes', 'cn': '\u819d\u4e0d\u8d85\u811a\u5c16'},
        },
        {
            'name': {'en': 'Step-up', 'cn': '\u4e0a\u53f0\u9636'},
            'target': {'en': 'Quadriceps, glutes', 'cn': '\u80a1\u56db\u5934\u808c\u3001\u81c0\u808c'},
            'setup': {'en': 'In front of a 10\u201320 cm step.', 'cn': '\u9762\u5bf9 10\u201320 cm \u53f0\u9636\u7ad9\u7acb\u3002'},
            'action': {'en': 'Step up, full stand, step down slowly.', 'cn': '\u4e0a\u53f0\uff0c\u5b8c\u5168\u7ad9\u7acb\uff0c\u7f13\u6162\u4e0b\u53f0\u3002'},
            'dose': '8\u201310 / leg \u00d7 2',
            'progress': {'en': 'Higher step', 'cn': '\u52a0\u9ad8\u53f0\u9636'},
            'regress': {'en': 'Lower step', 'cn': '\u964d\u4f4e\u53f0\u9636'},
            'safety': {'en': 'Rail or wall nearby', 'cn': '\u65c1\u8fb9\u6709\u6276\u624b\u6216\u5899'},
        },
    ]),

    # ── Upper-limb strength ──
    ('strength_upper', {
        'en': 'Resistance \u2014 Upper Limb',
        'cn': '\u6297\u963b\u8bad\u7ec3\uff08\u4e0a\u80a2\uff09',
    }, [
        {
            'name': {'en': 'Wall Push-up', 'cn': '\u9760\u5899\u4fef\u5367\u6491'},
            'target': {'en': 'Pectorals, triceps, deltoids', 'cn': '\u80f8\u5927\u808c\u3001\u80b1\u4e09\u5934\u808c\u3001\u4e09\u89d2\u808c'},
            'setup': {'en': 'Arm-length from wall, palms at shoulder height.', 'cn': '\u79bb\u5899\u4e00\u81c2\u5c55\uff0c\u638c\u4e0e\u80a9\u540c\u9ad8\u3002'},
            'action': {'en': 'Bend elbows, bring chest to wall, push back.', 'cn': '\u5c48\u80f3\uff0c\u80f8\u90e8\u9760\u5899\uff0c\u518d\u63a8\u56de\u3002'},
            'dose': '10\u201315 \u00d7 2',
            'progress': {'en': 'Feet further back', 'cn': '\u53cc\u811a\u540e\u79fb'},
            'regress': {'en': 'Closer to wall', 'cn': '\u9760\u8fd1\u5899\u9762'},
            'safety': {'en': 'Keep core engaged', 'cn': '\u6536\u7d27\u6838\u5fc3'},
        },
        {
            'name': {'en': 'Seated Band Row', 'cn': '\u5750\u59ff\u5f39\u529b\u5e26\u5212\u8239'},
            'target': {'en': 'Rhomboids, latissimus', 'cn': '\u83f1\u5f62\u808c\u3001\u80cc\u9614\u808c'},
            'setup': {'en': 'Seated, band around feet, elbows in.', 'cn': '\u5750\u4f4d\uff0c\u5f39\u529b\u5e26\u7ed5\u8fc7\u53cc\u811a\uff0c\u80f3\u8d34\u8eab\u3002'},
            'action': {'en': 'Pull band to waist, squeeze shoulder blades.', 'cn': '\u62c9\u5f39\u529b\u5e26\u81f3\u8170\u90e8\uff0c\u6536\u7d27\u80a9\u8140\u9aa8\u3002'},
            'dose': '10\u201312 \u00d7 2',
            'progress': {'en': 'Stiffer band', 'cn': '\u66f4\u7c97\u5f39\u529b\u5e26'},
            'regress': {'en': 'Lighter band', 'cn': '\u66f4\u8f7b\u5f39\u529b\u5e26'},
            'safety': {'en': 'Upright posture, no rounding', 'cn': '\u4fdd\u6301\u631a\u76f4\uff0c\u52ff\u5f2f\u8170'},
        },
        {
            'name': {'en': 'Shoulder Press (Band)', 'cn': '\u5f39\u529b\u5e26\u80a9\u4e0a\u63a8'},
            'target': {'en': 'Deltoids, triceps', 'cn': '\u4e09\u89d2\u808c\u3001\u80b1\u4e09\u5934\u808c'},
            'setup': {'en': 'Seated or standing, band under feet.', 'cn': '\u5750\u4f4d\u6216\u7ad9\u7acb\uff0c\u5f39\u529b\u5e26\u8e0f\u4e8e\u53cc\u811a\u4e0b\u3002'},
            'action': {'en': 'Press overhead, lower slowly to shoulders.', 'cn': '\u4e0a\u63a8\u81f3\u5934\u9876\uff0c\u7f13\u6162\u4e0b\u843d\u81f3\u80a9\u3002'},
            'dose': '8\u201310 \u00d7 2',
            'progress': {'en': 'Stiffer band', 'cn': '\u66f4\u7c97\u5f39\u529b\u5e26'},
            'regress': {'en': 'Smaller range', 'cn': '\u51cf\u5c0f\u5e45\u5ea6'},
            'safety': {'en': 'Stop if shoulder pain', 'cn': '\u80a9\u75db\u5373\u505c'},
        },
        {
            'name': {'en': 'Band Pull-apart', 'cn': '\u5f39\u529b\u5e26\u5916\u5c55'},
            'target': {'en': 'Rear deltoids, rhomboids', 'cn': '\u540e\u4e09\u89d2\u808c\u3001\u83f1\u5f62\u808c'},
            'setup': {'en': 'Stand, band at chest height, arms forward.', 'cn': '\u7ad9\u7acb\uff0c\u5f39\u529b\u5e26\u7f6e\u4e8e\u80f8\u524d\uff0c\u53cc\u81c2\u524d\u4f38\u3002'},
            'action': {'en': 'Pull band apart to sides, return slowly.', 'cn': '\u5c06\u5f39\u529b\u5e26\u5411\u4e24\u4fa7\u62c9\u5f00\uff0c\u7f13\u6162\u590d\u4f4d\u3002'},
            'dose': '10 \u00d7 2',
            'progress': {'en': 'Wider grip', 'cn': '\u66f4\u5bbd\u63e1\u8ddd'},
            'regress': {'en': 'Narrower grip', 'cn': '\u66f4\u7a84\u63e1\u8ddd'},
            'safety': {'en': 'Shoulders down, no shrug', 'cn': '\u6c89\u80a9\uff0c\u52ff\u7b7c\u80a9'},
        },
        {
            'name': {'en': 'Chair Triceps Dip', 'cn': '\u5ea7\u6905\u80b1\u4e09\u5934\u8e0d\u4f38'},
            'target': {'en': 'Triceps', 'cn': '\u80b1\u4e09\u5934\u808c'},
            'setup': {'en': 'Seated at chair edge, hands gripping seat edge.', 'cn': '\u5750\u4e8e\u6905\u8fb9\uff0c\u53cc\u624b\u6293\u4f4f\u5ea7\u6905\u8fb9\u7f18\u3002'},
            'action': {'en': 'Slide hips forward, bend elbows 5\u201310 cm, push up.', 'cn': '\u9ac4\u90e8\u524d\u79fb\uff0c\u5c48\u80f3 5\u201310 cm\uff0c\u518d\u63a8\u8d77\u3002'},
            'dose': '8\u201310 \u00d7 2',
            'progress': {'en': 'Feet further out', 'cn': '\u53cc\u811a\u524d\u79fb'},
            'regress': {'en': 'Smaller dip', 'cn': '\u51cf\u5c0f\u4e0b\u964d\u5e45\u5ea6'},
            'safety': {'en': 'Chair against wall', 'cn': '\u6905\u5b50\u9760\u5899'},
        },
    ]),

    # ── Balance ──
    ('balance', {
        'en': 'Balance',
        'cn': '\u5e73\u8861\u8bad\u7ec3',
    }, [
        {
            'name': {'en': 'Single-Leg Stand', 'cn': '\u5355\u817f\u7ad9\u7acb'},
            'target': {'en': 'Static balance', 'cn': '\u9759\u6001\u5e73\u8861'},
            'setup': {'en': 'Stand behind a sturdy chair.', 'cn': '\u7ad9\u4e8e\u7a33\u56fa\u6905\u80cc\u540e\u3002'},
            'action': {'en': 'Lift one foot, hold, lower. Alternate legs.', 'cn': '\u62ac\u8d77\u4e00\u811a\uff0c\u4fdd\u6301\uff0c\u4e0b\u843d\u3002\u4e24\u4fa7\u4ea4\u66ff\u3002'},
            'dose': 'Hold 10\u201330 s / leg \u00d7 3',
            'progress': {'en': 'Eyes closed / no support', 'cn': '\u95ed\u773c / \u4e0d\u6276\u7269'},
            'regress': {'en': 'Two-hand support', 'cn': '\u53cc\u624b\u6276\u6905'},
            'safety': {'en': 'Always near support', 'cn': '\u59cb\u7ec8\u9760\u8fd1\u652f\u6491'},
        },
        {
            'name': {'en': 'Tandem Stance', 'cn': '\u4e32\u8054\u7ad9\u7acb'},
            'target': {'en': 'Static balance', 'cn': '\u9759\u6001\u5e73\u8861'},
            'setup': {'en': 'Stand heel-to-toe, near wall.', 'cn': '\u811a\u8ddf\u8d34\u811a\u5c16\u7ad9\u7acb\uff0c\u9760\u8fd1\u5899\u9762\u3002'},
            'action': {'en': 'Hold the tandem position, switch lead foot.', 'cn': '\u4fdd\u6301\u4e32\u8054\u59ff\u52bf\uff0c\u4ea4\u6362\u524d\u540e\u811a\u3002'},
            'dose': 'Hold 20\u201330 s \u00d7 3',
            'progress': {'en': 'Eyes closed', 'cn': '\u95ed\u773c'},
            'regress': {'en': 'Semi-tandem', 'cn': '\u534a\u4e32\u8054'},
            'safety': {'en': 'Near wall for grab', 'cn': '\u9760\u5899\u4ee5\u5907\u6276'},
        },
        {
            'name': {'en': 'Heel-to-Toe Walk', 'cn': '\u811a\u8ddf\u811a\u5c16\u8d70'},
            'target': {'en': 'Dynamic balance', 'cn': '\u52a8\u6001\u5e73\u8861'},
            'setup': {'en': 'Along a wall or hallway.', 'cn': '\u6cbf\u5899\u6216\u8d70\u9053\u8fdb\u884c\u3002'},
            'action': {'en': 'Walk placing heel to toe in a line.', 'cn': '\u6cbf\u76f4\u7ebf\u8d70\uff0c\u811a\u8ddf\u8d34\u811a\u5c16\u3002'},
            'dose': '10 steps \u00d7 3',
            'progress': {'en': 'Backward walk', 'cn': '\u5012\u9000\u8d70'},
            'regress': {'en': 'Wider base', 'cn': '\u52a0\u5bbd\u6b65\u5e45'},
            'safety': {'en': 'Wall on one side', 'cn': '\u4e00\u4fa7\u9760\u5899'},
        },
        {
            'name': {'en': 'Weight Shift', 'cn': '\u91cd\u5fc3\u8f6c\u79fb'},
            'target': {'en': 'Dynamic balance', 'cn': '\u52a8\u6001\u5e73\u8861'},
            'setup': {'en': 'Stand, feet shoulder-width, near support.', 'cn': '\u7ad9\u7acb\uff0c\u53cc\u811a\u4e0e\u80a9\u540c\u5bbd\uff0c\u9760\u8fd1\u652f\u6491\u3002'},
            'action': {'en': 'Shift weight side to side smoothly.', 'cn': '\u5e73\u7a33\u5730\u5de6\u53f3\u8f6c\u79fb\u91cd\u5fc3\u3002'},
            'dose': '10 / side \u00d7 2',
            'progress': {'en': 'Wider stance', 'cn': '\u52a0\u5bbd\u7ad9\u59ff'},
            'regress': {'en': 'Hold support', 'cn': '\u6276\u4f4f\u652f\u6491'},
            'safety': {'en': 'Controlled tempo', 'cn': '\u63a7\u5236\u8282\u594f'},
        },
        {
            'name': {'en': 'Clock Reach', 'cn': '\u65f6\u949f\u4f38\u624b'},
            'target': {'en': 'Dynamic balance', 'cn': '\u52a8\u6001\u5e73\u8861'},
            'setup': {'en': 'Imagine a clock face on the floor.', 'cn': '\u60f3\u8c61\u5730\u9762\u6709\u4e00\u4e2a\u65f6\u949f\u3002'},
            'action': {'en': 'Reach one foot to 12, 3, 6, 9 positions.', 'cn': '\u4e00\u811a\u4f38\u5411 12\u30013\u30016\u30019 \u70b9\u65b9\u5411\u3002'},
            'dose': '8 / side \u00d7 2',
            'progress': {'en': 'Further reach', 'cn': '\u66f4\u8fdc\u4f38\u624b'},
            'regress': {'en': 'Shorter reach', 'cn': '\u66f4\u8fd1\u4f38\u624b'},
            'safety': {'en': 'Opposite hand on chair', 'cn': '\u53e6\u4e00\u624b\u6276\u6905'},
        },
        {
            'name': {'en': 'Side Step', 'cn': '\u4fa7\u6b65\u8d70'},
            'target': {'en': 'Dynamic balance', 'cn': '\u52a8\u6001\u5e73\u8861'},
            'setup': {'en': 'Stand, feet hip-width, near wall.', 'cn': '\u7ad9\u7acb\uff0c\u53cc\u811a\u4e0e\u9ac4\u540c\u5bbd\uff0c\u9760\u8fd1\u5899\u9762\u3002'},
            'action': {'en': 'Step sideways 10 steps, return.', 'cn': '\u5411\u4fa7\u9762\u8d70 10 \u6b65\uff0c\u518d\u8fd4\u56de\u3002'},
            'dose': '10 / side \u00d7 2',
            'progress': {'en': 'Resistance band at ankles', 'cn': '\u811a\u8155\u52a0\u5f39\u529b\u5e26'},
            'regress': {'en': 'Shorter steps', 'cn': '\u66f4\u5c0f\u6b65\u5e45'},
            'safety': {'en': 'Do not cross legs', 'cn': '\u52ff\u4ea4\u53c9\u53cc\u817f'},
        },
    ]),

    # ── Flexibility ──
    ('flexibility', {
        'en': 'Flexibility',
        'cn': '\u67d4\u97e7\u6027\u8bad\u7ec3',
    }, [
        {
            'name': {'en': 'Calf Stretch', 'cn': '\u5c0f\u817f\u725b\u4f38'},
            'target': {'en': 'Gastrocnemius, soleus', 'cn': '\u8153\u80a0\u808c\u3001\u6bd4\u76ee\u9c7c\u808c'},
            'setup': {'en': 'Stand facing wall, one foot back, straight knee.', 'cn': '\u9762\u5899\u7ad9\u7acb\uff0c\u4e00\u811a\u540e\u9000\uff0c\u819d\u4f38\u76f4\u3002'},
            'action': {'en': 'Lean forward, feel stretch in back calf.', 'cn': '\u524d\u503e\uff0c\u611f\u53d7\u540e\u4fa7\u5c0f\u817f\u725b\u4f38\u3002'},
            'dose': 'Hold 20\u201330 s \u00d7 2 / leg',
            'progress': {'en': 'Deeper lean', 'cn': '\u66f4\u6df1\u524d\u503e'},
            'regress': {'en': 'Less lean', 'cn': '\u51cf\u5c11\u524d\u503e'},
            'safety': {'en': 'No bouncing', 'cn': '\u52ff\u5f39\u9707'},
        },
        {
            'name': {'en': 'Hamstring Stretch', 'cn': '\u8158\u7ef3\u808c\u725b\u4f38'},
            'target': {'en': 'Hamstrings', 'cn': '\u8158\u7ef3\u808c'},
            'setup': {'en': 'Seated, one leg extended.', 'cn': '\u5750\u4f4d\uff0c\u4e00\u817f\u4f38\u76f4\u3002'},
            'action': {'en': 'Hinge forward from hips, reach for toes.', 'cn': '\u4ece\u9ac4\u90e8\u524d\u5c48\uff0c\u624b\u89e6\u811a\u5c16\u3002'},
            'dose': 'Hold 20\u201330 s \u00d7 2 / leg',
            'progress': {'en': 'Straighten knee more', 'cn': '\u819d\u5173\u8282\u66f4\u76f4'},
            'regress': {'en': 'Slight knee bend', 'cn': '\u819d\u5fae\u5c48'},
            'safety': {'en': 'No bouncing; back straight', 'cn': '\u52ff\u5f39\u9707\uff1b\u4fdd\u6301\u80cc\u76f4'},
        },
        {
            'name': {'en': 'Chest / Pec Stretch', 'cn': '\u80f8\u90e8\u725b\u4f38'},
            'target': {'en': 'Pectorals', 'cn': '\u80f8\u5927\u808c'},
            'setup': {'en': 'Stand in a doorway, forearm on frame.', 'cn': '\u7ad9\u4e8e\u95e8\u6846\uff0c\u524d\u81c2\u8d34\u95e8\u6846\u3002'},
            'action': {'en': 'Gently turn away, feel stretch across chest.', 'cn': '\u8f7b\u8f6c\u8eab\u4f53\uff0c\u611f\u53d7\u80f8\u90e8\u725b\u4f38\u3002'},
            'dose': 'Hold 20\u201330 s \u00d7 2 / side',
            'progress': {'en': 'Higher arm on frame', 'cn': '\u624b\u81c2\u52a0\u9ad8'},
            'regress': {'en': 'Lower arm position', 'cn': '\u624b\u81c2\u964d\u4f4e'},
            'safety': {'en': 'Gentle, no pain', 'cn': '\u8f7b\u67d4\u62c9\u4f38\uff0c\u65e0\u75db'},
        },
        {
            'name': {'en': 'Hip Flexor Stretch', 'cn': '\u9acb\u5c48\u808c\u725b\u4f38'},
            'target': {'en': 'Iliopsoas', 'cn': '\u9acb\u8170\u808c'},
            'setup': {'en': 'Standing lunge, back knee straight.', 'cn': '\u5f6a\u6b65\u7ad9\u7acb\uff0c\u540e\u817f\u819d\u4f38\u76f4\u3002'},
            'action': {'en': 'Tuck pelvis, shift weight forward gently.', 'cn': '\u6536\u9aa8\u76c8\uff0c\u8f7b\u8f7b\u524d\u79fb\u91cd\u5fc3\u3002'},
            'dose': 'Hold 20\u201330 s \u00d7 2 / leg',
            'progress': {'en': 'Deeper lunge', 'cn': '\u66f4\u6df1\u5f6a\u6b65'},
            'regress': {'en': 'Shorter stance', 'cn': '\u66f4\u77ed\u6b65\u5e45'},
            'safety': {'en': 'Chair for balance', 'cn': '\u6905\u5b50\u8f85\u52a9\u5e73\u8861'},
        },
        {
            'name': {'en': 'Neck Range of Motion', 'cn': '\u9888\u90e8\u6d3b\u52a8\u5ea6'},
            'target': {'en': 'Cervical muscles', 'cn': '\u9888\u90e8\u808c\u7fa4'},
            'setup': {'en': 'Seated, shoulders relaxed.', 'cn': '\u5750\u4f4d\uff0c\u53cc\u80a9\u653e\u677e\u3002'},
            'action': {'en': 'Slow rotations, side bends, chin tucks.', 'cn': '\u7f13\u6162\u65cb\u8f6c\u3001\u4fa7\u5c48\u3001\u6536\u4e0b\u5df4\u3002'},
            'dose': '5 reps each \u00d7 1\u20132',
            'progress': {'en': 'Full pain-free range', 'cn': '\u65e0\u75db\u5168\u8303\u56f4'},
            'regress': {'en': 'Smaller range', 'cn': '\u51cf\u5c0f\u8303\u56f4'},
            'safety': {'en': 'No forced end-range', 'cn': '\u52ff\u5f3a\u884c\u5230\u6781\u9650'},
        },
    ]),

    # ── Aerobic ──
    ('aerobic', {
        'en': 'Aerobic',
        'cn': '\u6709\u6c27\u8bad\u7ec3',
    }, [
        {
            'name': {'en': 'Marching in Place', 'cn': '\u539f\u5730\u8e0f\u6b65'},
            'target': {'en': 'Cardiovascular', 'cn': '\u5fc3\u80ba\u8010\u529b'},
            'setup': {'en': 'Stand or sit, upright posture.', 'cn': '\u7ad9\u7acb\u6216\u5750\u4f4d\uff0c\u4fdd\u6301\u631a\u76f4\u3002'},
            'action': {'en': 'Alternate lifting knees to hip height.', 'cn': '\u4ea4\u66ff\u62ac\u819d\u81f3\u9ac4\u9ad8\u5ea6\u3002'},
            'dose': '1\u20133 min \u00d7 2\u20133',
            'progress': {'en': 'Higher knees / faster', 'cn': '\u62ac\u819d\u66f4\u9ad8 / \u52a0\u5feb'},
            'regress': {'en': 'Seated march', 'cn': '\u5750\u4f4d\u8e0f\u6b65'},
            'safety': {'en': 'RPE 11\u201313', 'cn': 'RPE 11\u201313'},
        },
        {
            'name': {'en': 'Step-up Circuit', 'cn': '\u53f0\u9636\u5faa\u73af'},
            'target': {'en': 'Cardiovascular, legs', 'cn': '\u5fc3\u80ba\u8010\u529b\u3001\u4e0b\u80a2'},
            'setup': {'en': 'In front of a 10\u201315 cm step, rail nearby.', 'cn': '\u9762\u5bf9 10\u201315 cm \u53f0\u9636\uff0c\u65c1\u8fb9\u6709\u6263\u624b\u3002'},
            'action': {'en': 'Step up and down at steady rhythm.', 'cn': '\u4ee5\u7a33\u5b9a\u8282\u594f\u4e0a\u4e0b\u53f0\u9636\u3002'},
            'dose': '1\u20133 min \u00d7 2',
            'progress': {'en': 'Faster pace', 'cn': '\u52a0\u5feb\u901f\u5ea6'},
            'regress': {'en': 'Lower step', 'cn': '\u964d\u4f4e\u53f0\u9636'},
            'safety': {'en': 'Hold rail if needed', 'cn': '\u9700\u8981\u65f6\u6263\u6263\u624b'},
        },
        {
            'name': {'en': 'Brisk Walk', 'cn': '\u5feb\u6b65\u8d70'},
            'target': {'en': 'Cardiovascular', 'cn': '\u5fc3\u80ba\u8010\u529b'},
            'setup': {'en': 'Flat, well-lit path; suitable footwear.', 'cn': '\u5e73\u5766\u3001\u7167\u660e\u8db3\u591f\u7684\u8def\u9762\uff1b\u5408\u9002\u978b\u5b50\u3002'},
            'action': {'en': 'Walk at a pace where talking is slightly effortful.', 'cn': '\u4ee5\u8bf4\u8bdd\u7a0d\u611f\u8d39\u529b\u7684\u901f\u5ea6\u6b65\u884c\u3002'},
            'dose': '10\u201330 min',
            'progress': {'en': 'Longer / faster', 'cn': '\u66f4\u957f / \u66f4\u5feb'},
            'regress': {'en': 'Shorter duration', 'cn': '\u51cf\u77ed\u65f6\u95f4'},
            'safety': {'en': 'Carry phone; avoid uneven ground', 'cn': '\u968f\u8eab\u643a\u5e26\u624b\u673a\uff1b\u907f\u514d\u5751\u6d3c\u8def\u9762'},
        },
        {
            'name': {'en': 'Seated Cycling', 'cn': '\u5750\u59ff\u8e0f\u8f66'},
            'target': {'en': 'Cardiovascular', 'cn': '\u5fc3\u80ba\u8010\u529b'},
            'setup': {'en': 'Stationary bike, seat at hip-knee level.', 'cn': '\u56fa\u5b9a\u8e0f\u8f66\uff0c\u5ea7\u4f4d\u8c03\u81f3\u9ac4\u819d\u540c\u9ad8\u3002'},
            'action': {'en': 'Cycle at moderate resistance, steady pace.', 'cn': '\u4e2d\u7b49\u963b\u529b\u3001\u7a33\u5b9a\u8e0f\u9891\u8e0f\u8f66\u3002'},
            'dose': '5\u201310 min',
            'progress': {'en': 'Higher resistance', 'cn': '\u52a0\u5927\u963b\u529b'},
            'regress': {'en': 'Shorter duration', 'cn': '\u51cf\u77ed\u65f6\u95f4'},
            'safety': {'en': 'RPE 12\u201314', 'cn': 'RPE 12\u201314'},
        },
    ]),
]


def build_exercise_library(lang='en'):
    """Return a list of story flowables for the exercise library section.

    lang: 'en' for English, 'cn' for Chinese.
    Uses styles/helpers from core (imported lazily to avoid circular import).
    """
    from core import (P, SP, section_banner, sub_header, note, cols,
                      make_table, s_th, s_td, s_td_c, s_small, s_field,
                      ACCENT, ACCENT_DARK, ACCENT_LIGHT, GREY_LINE, BASE_FONT, BOLD_FONT,
                      FULL_W, colors)
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors as rl_colors

    story = []

    if lang == 'cn':
        title = '\u5c45\u5bb6\u8fd0\u52a8\u5e93'
        intro = ('\u4ee5\u4e0b\u7cbe\u9009 {n} \u4e2a\u9002\u5408\u8001\u5e74\u4eba\u7684\u5c45\u5bb6\u5b89\u5168\u52a8\u4f5c\uff0c'
                 '\u5206\u4e3a\u4e94\u7c7b\u3002\u6bcf\u4e2a\u52a8\u4f5c\u5747\u6807\u6ce8\u76ee\u6807\u808c\u7fa4\u3001'
                 '\u5242\u91cf\u3001\u8fdb\u9636\u4e0e\u9000\u9636\uff0c\u4f9b\u6cbb\u7597\u5e08\u6839\u636e\u8bc4\u4f30\u7ed3\u679c'
                 '\u4e2a\u6027\u5316\u5904\u65b9\u3002')
        lbl_target = '\u76ee\u6807'
        lbl_instr = '\u52a8\u4f5c\u8981\u9886'
        lbl_dose = '\u5242\u91cf'
        lbl_prog = '\u8fdb\u9636 \u2191'
        lbl_reg = '\u9000\u9636 \u2193'
        warmup = ('\u70ed\u8eab\uff1a5\u201310 \u5206\u949f\u4f4e\u5f3a\u5ea6\u6d3b\u52a8\uff08\u539f\u5730\u8e0f\u6b65\u3001'
                  '\u5173\u8282\u6d3b\u52a8\uff09\u3002\u653e\u677e\uff1a\u7ec3\u540e\u8fdb\u884c\u67d4\u97e7\u6027\u725b\u4f38\u3002')
        caution = ('\u6ce8\u610f\uff1a\u6240\u6709\u5e73\u8861\u52a8\u4f5c\u59cb\u7ec8\u9760\u8fd1\u6263\u624b\u6216\u5899\u9762\u3002'
                   '\u51fa\u73b0\u75db\u3001\u5934\u6655\u6216\u5fc3\u60b8\u65f6\u7acb\u5373\u505c\u6b62\u3002')
        safety_hdr = '\u4f7f\u7528\u8bf4\u660e'
    else:
        title = 'Home Exercise Library'
        intro = (f'{sum(len(c[2]) for c in EXERCISE_CATEGORIES)} curated, senior-safe home exercises '
                 'in five categories. Each entry lists the target, dosage, progression, and '
                 'regression for individualised prescription based on assessment findings.')
        lbl_target = 'Target'
        lbl_instr = 'Key cues'
        lbl_dose = 'Dose'
        lbl_prog = 'Progress \u2191'
        lbl_reg = 'Regress \u2193'
        warmup = ('Warm-up: 5\u201310 min low-intensity (marching, joint mobility). '
                  'Cool-down: stretch after session.')
        caution = ('Caution: always stay near support for balance exercises. '
                   'Stop immediately if pain, dizziness, or palpitations occur.')
        safety_hdr = 'Usage notes'

    # Section banner
    story.extend(section_banner('', title, toc=True))
    story.append(P(intro))
    story.append(SP(8))

    # Usage notes box
    notes_tbl = Table([
        [P(f'<b>{safety_hdr}</b>', s_td)],
        [P(warmup, s_small)],
        [P(caution, s_small)],
    ], colWidths=[FULL_W])
    notes_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, ACCENT),
        ('BACKGROUND', (0, 0), (0, 0), ACCENT),
        ('TEXTCOLOR', (0, 0), (0, 0), rl_colors.white),
        ('FONTNAME', (0, 0), (0, 0), BOLD_FONT),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(notes_tbl)
    story.append(SP(10))

    n = 0
    for _key, cat_name, exercises in EXERCISE_CATEGORIES:
        story.extend(sub_header(cat_name[lang]))

        header = [
            P('<b>#</b>', s_th),
            P(f'<b>{lbl_target}</b>', s_th),
            P(f'<b>{lbl_instr}</b>', s_th),
            P(f'<b>{lbl_dose}</b>', s_th),
            P(f'<b>{lbl_prog} / {lbl_reg}</b>', s_th),
        ]
        rows = [header]
        for ex in exercises:
            n += 1
            name_target = f'<b>{ex["name"][lang]}</b><br/><font size="7" color="#555555">{ex["target"][lang]}</font>'
            instr = f'{ex["setup"][lang]} {ex["action"][lang]}'
            prog_reg = f'\u2191 {ex["progress"][lang]}<br/>\u2193 {ex["regress"][lang]}'
            rows.append([
                P(str(n), s_td_c),
                P(name_target, s_td),
                P(instr, s_td),
                P(ex['dose'], s_td_c),
                P(prog_reg, s_small),
            ])

        tbl = Table(rows, colWidths=cols(1, 3.5, 5.5, 2, 4))
        cmds = [
            ('GRID', (0, 0), (-1, -1), 0.5, GREY_LINE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('FONTNAME', (0, 0), (-1, -1), BASE_FONT),
            ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
            ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.white),
            ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('LINEBELOW', (0, 0), (-1, 0), 1.4, ACCENT_DARK),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('LEADING', (0, 0), (-1, -1), 11),
        ]
        for r in range(1, len(rows)):
            if r % 2 == 0:
                cmds.append(('BACKGROUND', (0, r), (-1, r), ACCENT_LIGHT))
        tbl.setStyle(TableStyle(cmds))
        story.append(tbl)
        story.append(SP(8))

    return story
