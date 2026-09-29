from domain.alerts import Alert, AlertObserver


def _msg(a: Alert):
    return f"{a.service}: {a.metric} = {a.value:.0f}% (umbral {a.threshold:.0f}%)"


class EmailAlert(AlertObserver):
    def update(self, alert: Alert):
        print(f"  [EMAIL] {_msg(alert)}")


class SlackAlert(AlertObserver):
    def update(self, alert: Alert):
        print(f"  [SLACK] {_msg(alert)}")


class SMSAlert(AlertObserver):          
    def update(self, alert: Alert):
        print(f"  [SMS] {_msg(alert)}")
