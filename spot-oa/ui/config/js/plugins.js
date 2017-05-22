// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const React = require('react');
const ReactDOM = require('react-dom');

const SpotActions = require('../../js/actions/SpotActions');
const SpotUtils = require('../../js/utils/SpotUtils');
const EdInActions = require('../../js/actions/EdInActions');
const DateInput = require('../../js/components/DateInput.react');
const MainMenu = require('../../js/menu/components/MainMenu.react');

ReactDOM.render(
  <MainMenu />,
  document.getElementById('main-menu')
);

ReactDOM.render(
    (
      <form className="form-inline">
        <div className="form-group">
          <label htmlFor="dataDatePicker">Data Date:</label>
          <div className="input-group input-group-xs">
            <DateInput id="dataDatePicker" />
            <div className="input-group-addon">
              <span className="glyphicon glyphicon-calendar" aria-hidden="true"></span>
            </div>
          </div>
        </div>
      </form>
    ),
    document.getElementById('nav_form')
);

// Build and Render Edge Investigation's panels
const PanelRow = require('../../js/components/PanelRow.react');
const Panel = require('../../js/components/Panel.react');
// const WidgetController = require('../../js/components/WidgetController.react');
const PluginController = require('./components/PluginController.react');

ReactDOM.render(
  <div id="spot-content">
    <PanelRow maximized>
      <Panel title="Plugins" container className="col-md-12">
        <PluginController />
      </Panel>
    </PanelRow>
  </div>,
  document.getElementById('spot-content-wrapper')
);

// Set search criteria
var date;

date = SpotUtils.getCurrentDate();

SpotActions.setDate(date);
EdInActions.getWidgets('scoring,menu', '');
