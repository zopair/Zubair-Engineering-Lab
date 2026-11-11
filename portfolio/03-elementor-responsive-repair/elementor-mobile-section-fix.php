<?php
/**
 * Plugin Name: Zubair Elementor Mobile Section Repair
 * Description: Enqueues a narrowly scoped responsive fix for one Elementor section.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Load the section-specific stylesheet only when Elementor is active.
 *
 * Replace the target Elementor element ID in the CSS with the ID from the
 * client's page before deployment. This plugin does not edit page content.
 */
function zopair_enqueue_elementor_mobile_section_fix(): void
{
    if (!did_action('elementor/loaded')) {
        return;
    }

    $relative_path = 'assets/elementor-mobile-fix.css';
    $absolute_path = plugin_dir_path(__FILE__) . $relative_path;
    $version = file_exists($absolute_path) ? (string) filemtime($absolute_path) : '1.0.0';

    wp_enqueue_style(
        'zopair-elementor-mobile-section-fix',
        plugin_dir_url(__FILE__) . $relative_path,
        array(),
        $version
    );
}
add_action('wp_enqueue_scripts', 'zopair_enqueue_elementor_mobile_section_fix', 30);
