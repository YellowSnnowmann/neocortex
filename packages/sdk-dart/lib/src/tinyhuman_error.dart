class TinyHumanError implements Exception {
  final String message;
  final int status;
  final String body;

  TinyHumanError(this.message, this.status, [this.body = '']);

  @override
  String toString() => 'TinyHumanError($status): $message';
}
