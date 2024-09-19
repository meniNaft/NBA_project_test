from seeds.seed import run_seed
from flask import Flask
from controllers.player_controller import player_blueprint
from controllers.team_controller import team_blueprint

app = Flask(__name__)
if __name__ == '__main__':
    run_seed()
    app.register_blueprint(player_blueprint, url_prefix="/api/players")
    app.register_blueprint(team_blueprint, url_prefix="/api/teams")
    app.run(debug=True, use_reloader=False)
