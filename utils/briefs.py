from classes.player import teams, traits


def teams_brief():
    mapper = map(
        lambda team: f'{team.get("call")[0]}{" "*(8 - len(team.get("call")[0]))}:: {team.get("name")}\n', teams())
    t = f'```{"".join(mapper)}```'
    teams_brief = ["Prebuilt Teams Available:", t]
    return teams_brief


def traits_brief():
    t = f'```{", ".join(traits())}```'
    traits_brief = ["Traits Available:", t]
    return traits_brief
