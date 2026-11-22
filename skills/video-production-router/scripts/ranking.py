"""Scoped decision views over the existing arsenal; never dispatches a tool."""

PRODUCTION_AXES = ('quality', 'control', 'repeatability', 'speed', 'cost')
TRIAL_AXES = ('fit', 'readiness', 'test_value')
STATUSES = {'production', 'reserve', 'trial', 'excluded'}
ACCESS = {'local', 'confirm', 'paid'}


def validate_rankings(facets):
    for profile_id, profile in facets.get('rankings', {}).items():
        weights = profile['weights']
        if set(weights) != set(PRODUCTION_AXES) or any(type(weight) is not int or weight < 1 for weight in weights.values()):
            raise ValueError('Invalid ranking weights: ' + profile_id)
        if not profile['title'].strip() or not profile['scope'].strip() or not profile['entries']:
            raise ValueError('Ranking requires title, scope and entries: ' + profile_id)
        seen = set()
        for entry in profile['entries']:
            tool, status = entry['tool'], entry['status']
            if tool in seen or tool not in facets['tools'] or status not in STATUSES or entry['access'] not in ACCESS:
                raise ValueError('Invalid ranking entry: ' + profile_id + '/' + tool)
            seen.add(tool)
            if not entry['reason'].strip():
                raise ValueError('Ranking requires a reason: ' + tool)
            application = find_application(facets['tools'][tool], entry.get('application'))
            if status in {'production', 'reserve'} and (
                application is None or application['evidence'] != 'tested'
                or application['technical']['status'] == 'failed'
                or application['owner_evaluation']['status'] == 'rejected'
            ):
                raise ValueError('Ranking requires usable tested application: ' + tool)
            if status == 'trial' and not entry.get('test', '').strip():
                raise ValueError('Trial ranking requires a concrete test: ' + tool)
            axes = TRIAL_AXES if status == 'trial' else () if status == 'excluded' else PRODUCTION_AXES
            ratings = entry['ratings']
            if set(ratings) != set(axes) or any(
                value is not None and (type(value) is not int or not 1 <= value <= 5)
                for value in ratings.values()
            ):
                raise ValueError('Invalid ranking ratings: ' + tool)
            if status in {'production', 'reserve'} and ratings['quality'] is None:
                raise ValueError('Production ranking requires a quality assessment: ' + tool)


def find_application(tool_facets, application_id):
    if application_id is None:
        return None
    for application in tool_facets.get('applications', []):
        if application['id'] == application_id:
            return application
    raise ValueError('Unknown ranking application: ' + application_id)


def compare(entries, weights):
    # Use only axes observed for every option in this pool; missing data never give bonus points.
    axes = [axis for axis in weights if entries and all(row['ratings'][axis] is not None for row in entries)]
    for row in entries:
        row['score'] = (
            round(sum(row['ratings'][axis] * weights[axis] for axis in axes) / sum(weights[axis] for axis in axes), 2)
            if axes else None
        )
    entries.sort(key=lambda row: (row['score'] is None, -(row['score'] or 0)))
    return axes


def ranked_profile(profile, rows, rights, purpose, unavailable, confirmed, allow_paid, include_fallbacks):
    result = {'title': profile['title'], 'scope': profile['scope'], 'weights': profile['weights']}
    production, reserve, trials, excluded = [], [], [], []
    for item in profile['entries']:
        row = dict(item)
        tool = rows[row['tool']]
        application = find_application(tool['facets'], row.get('application'))
        row['name'] = tool['name']
        row['rights'] = rights(tool, purpose)
        row['sources'] = application['sources'] if application else (tool['review'] or {}).get('evidence', [])
        row['version'] = application['version'] if application else None
        row['resources'] = application['resources'] if application else None
        row['owner_evaluation'] = application['owner_evaluation'] if application else None
        row['blocking_reasons'] = []
        if row['status'] == 'excluded':
            row['blocking_reasons'].append('Excluded by retained studio decision')
            excluded.append(row)
            continue
        if row['tool'] in unavailable:
            row['blocking_reasons'].append('Unavailable in this production')
        if row['access'] in {'confirm', 'paid'} and row['tool'] not in confirmed:
            row['blocking_reasons'].append('Confirm access and setup first')
        if row['access'] == 'paid' and not allow_paid:
            row['blocking_reasons'].append('Paid routes are off for this comparison')
        if not row['rights']['matches_filter']:
            row['blocking_reasons'].append('Retained rights do not match this use')
        if row['status'] == 'reserve' and not include_fallbacks:
            row['blocking_reasons'].append('Explicit reserve opt-in required')
        {'production': production, 'reserve': reserve, 'trial': trials}[row['status']].append(row)

    result['production_score_axes'] = compare(production, profile['weights'])
    result['reserve_score_axes'] = compare(reserve, profile['weights'])
    result['trial_score_axes'] = compare(trials, dict.fromkeys(TRIAL_AXES, 1))
    options = [row for row in production + reserve if not row['blocking_reasons']]
    test = next((row for row in trials if not row['blocking_reasons'] and row['score'] is not None), None)
    result.update(
        primary=options[0]['tool'] if options else None,
        fallback=options[1]['tool'] if len(options) > 1 else None,
        priority_test=trials[0]['tool'] if trials and trials[0]['score'] is not None else None,
        next_test=test['tool'] if test else None,
        production=production,
        reserve=reserve,
        trials=trials,
        excluded=excluded,
    )
    return result


def markdown(result):
    scores = (('Production', result['production'], PRODUCTION_AXES, result['production_score_axes']),
              ('Reserve', result['reserve'], PRODUCTION_AXES, result['reserve_score_axes']),
              ('Test queue', result['trials'], TRIAL_AXES, result['trial_score_axes']),
              ('Excluded', result['excluded'], (), ()))
    out = [f"# {result['title']}", '', result['scope'], '',
           f"Primary **{result['primary'] or 'none'}** · Fallback **{result['fallback'] or 'none'}** · First in queue **{result['priority_test'] or 'none'}** · Ready to test **{result['next_test'] or 'none'}**", '',
           'Ratings are scoped studio judgments. Dash means unknown. Check current access, rights and delivery requirements before use.', '']
    for label, entries, axes, compared in scores:
        if not entries:
            continue
        columns = ['Tool', 'Status', *axes, 'Score', 'Reason and evidence']
        out.extend([f'## {label}', ''])
        if compared:
            out.extend(['Score uses: ' + ', '.join(compared) + '.', ''])
        out.extend(['| ' + ' | '.join(columns) + ' |', '| ' + ' | '.join(['---'] * len(columns)) + ' |'])
        for row in entries:
            reason = row['reason']
            if row['blocking_reasons']:
                reason += ' Blocked: ' + '; '.join(row['blocking_reasons']) + '.'
            if row.get('test'):
                reason += ' Probe: ' + row['test']
            if row.get('version'):
                reason += ' Version: ' + row['version'] + '.'
            if row.get('owner_evaluation'):
                reason += ' Owner: ' + row['owner_evaluation']['scope']
            if row['resources']:
                for field, label in (('timing', 'Render timing'), ('time', 'Effort'), ('cost', 'Cost')):
                    note = row['resources'].get(field)
                    if note and note not in {'unknown', 'not_recorded_in_index', 'not_extracted'}:
                        reason += f' {label}: {note.rstrip(".")}.'
            if row['sources']:
                reason += ' ' + ', '.join(f'[{source}]({source})' for source in row['sources'])
            values = [row['name'], row['status'], *[str(row['ratings'][axis] or '—') for axis in axes],
                      str(row['score']) if row.get('score') is not None else '—', reason]
            out.append('| ' + ' | '.join(value.replace('|', r'\|') for value in values) + ' |')
        out.append('')
    return '\n'.join(out)
